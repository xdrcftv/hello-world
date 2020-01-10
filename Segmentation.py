import numpy as np
from glob import glob
from scipy import ndimage, misc
from PIL import Image, ImageDraw
import re
import copy

def binary(mask, th):
    mask[mask >= th] = 1
    mask[mask < th] = 0
    return mask

def check_arrays(array1, array2)
    exists = False
    for i in array1:
        if np.sum(i==array2)>0:
            exists =True
    return exists

def append_arrays(array1, array2):
    array = np.unique(np.append(array1, array2))
    return array

def find_path(points):
    point_array = np.array([])
    rm_idx = np.random.randint(len(points))
    current = points[rm_idx]
    points = np.delete(points, rm_idx, 0)
    empty = (len(points) == 0)
    point_array = np.append(point_array, current)
    radius_2 = 1 # sqaured radius
    while not empty:
        nearby_points = search_nearby(current, points, 1)
        while len(nearby_points) == 0: # no points nearby in that radius
            radius_2 += 1
            nearby_points = search_nearby(current, points, np.sqrt(radius_2))
        radius_2 = 1

        sampled_idx = np.random.randint(len(nearby_points))
        sampled_point = nearby_points[sampled_idx]
        rm_idx = np.where(np.all(points == sampled_point, axis = 1))
        points = np.delete(points, rm_idx, 0)
        current = sampled_point
        point_array = np.append(point_array, current)
        empty = (len(points) == 0)
    return point_array

def determine_direction(sort_points, is_positive):
    sum_line_integral = 0
    for i in range(len(sort_points) - 1):
        x_1 = sort_points[i, 0]
        x_2 = sort_points[i+1, 0]
        y_1 = sort_points[i, 1]
        y_2 = sort_points[i+1, 1]
        line_integral = (y_2 - y_1) * (x_2 + x_1)
        sum_line_integral += line_integral
    if sum_line_integral < 0:
        clock_wise = 0
    else:
        clock_wise = 1
    if not is_positive ^ clock_wise:
        sort_points = np.flip(sort_points, 0)
    return sort_points

def generate_points(npy):
    mask = binary(npy[:, 1024:], 0.5)
    mask = binary(ndimage.median_filter(mask, size = 2), 0.5)
    edges = np.zeros((512, 512))
    sparse_edges = np.zeros((512,512))
    for i in range(1,511):
        for j in range(1,511):
            if (np.sum(mask[i-1:i+2, j-1:j+2])>2)&(np.sum(mask[i-1:i+2,j-1:j+2])<6):
                edges[i,j]=1
            if (np.sum(mask[i-1:i+2, j-1:j+2])==5):
                sparse_edges[i,j] = 1

    idx_i, idx_j = (np.where(edges == 1))
    bm_coor = np.transpose(np.array([idx_j, idx_i]))
    sp_idx_i, sp_idx_j = (np.where(sparse_edges == 1))
    sparse_coor = np.transpose(np.array([sp_idx_j, sp_idx_i]))
    tmp_idx_array = []
    curv_points = []

    for i in range(0, len(bm_coor)):
        coor_dist = np.sqrt((bm_coor[:, 0] - bm_coor[i, 0])**2 + (bm_coor[:, 1] - bm_coor[i, 1])**2)
        tmp_idx = np.where(coor_dist <= 2)
        tmp_idx = tmp_idx[0]
        tmp_idx_array.append(tmp_idx)
    coor_empty = False
    del_idx = np.array([])
    curv_points.append(tmp_idx_array[0])
    tmp_idx_array = tmp_idx_array[1:]
    prev_len = 0

    while not coor_empty:
        for it in range(len(tmp_idx_array)):
            for jt in range(len(curv_points)):
                if check_arrays(curv_points[jt], tmp_idx_array[it]):
                    curv_points[jt] = append_arrays(curv_points[jt], tmp_idx_array[it])
                    del_idx = np.append(del_idx, it)
        tmp_idx_array = np.delete(tmp_idx_array, del_idx, 0).tolist()
        del_idx = np.array([])
        if len(tmp_idx_array) == 0:
           coor_empty = True
        elif prev_len == len(tmp_idx_array):
            curv_points.append(tmp_idx_array[0])
            tmp_idx_array = np.delete(tmp_idx_array, 0, 0).tolist()
        prev_len = len(tmp_idx_array)
    new_mask = np.zeros((512, 512))
    refined_Contour_data = []
    for num_p in range(len(curv_points)):
        raw_points = np.transpose(np.array([idx_j[curv_points[num_p]], idx_i[curv_points[num_p]]]))
        sort_points = np.reshape(find_path(raw_points), (-1, 2))
        img = Image.new('L', (512, 512))
        draw = ImageDraw.Draw(img)
        points = []
        coor = sort_points
        for i in range(0, len(coor)):
            points.append(tuple(coor[i]))
        points = tuple(points)
        draw.polygon((points), fill = 1)
        img = np.array(img)
        if np.max(new_mask + img) == 1:
            new_mask += img
            is_positive = True
        else:
            new_mask -= img
            is_positive = False
        direction_coor = determine_direction(sort_points, is_positive)
        refined_coor = direction_coor[np.sum(np.isin(direction_coor, sparse_coor), axis = 1) == 2]
        if len(refined_coor) == 0:
            refined_Contour_data.append(direction_coor)
        else:
            refined_Contour_data.append(refined_coor)
    return refined_Contour_data