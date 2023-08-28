#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:55:59 2023

@author: rya200
"""

from nilearn.maskers import MultiNiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure
from nilearn.maskers import NiftiMasker
from nilearn import datasets
from nilearn import plotting
from nilearn.regions import connected_label_regions
from nilearn import image
import numpy as np
import matplotlib as plt
# %%


aal = datasets.fetch_atlas_aal()
msdl = datasets.fetch_atlas_msdl()
fname = aal.maps
cmap = plt.cm.gist_ncar(np.linspace(0, 256, len(aal.labels) + 1))[1:]
plotting.plot_roi(fname,  display_mode="mosaic")


# %%
# single_region = image.math_img("np.where(img, np.isin(img, np.array(aal.indices[-10:], dtype='int')), 0)",
#                                img=fname, aal=aal)
# plotting.plot_roi(single_region)  # , cut_coords=[2, -40, -1])
# %%

# plotting.plot_prob_atlas(msdl.maps)

# %%

img = image.load_img(msdl.maps)

# %% Visualising MSDL in RSN

tmp_list = list()

lbls_vec = np.array(msdl.networks)
unique_lbls = np.unique(lbls_vec)

for uu in unique_lbls:
    tmp_list = list()
    reg_coord = list()
    for i in np.where(lbls_vec == uu)[0]:
        tmp_list.append(image.index_img(img, i))
        reg_coord.append(msdl.region_coords[i])
    # reg_coord = np.array(reg_coord)
    reg_coord = plotting.find_probabilistic_atlas_cut_coords(tmp_list)
    reg_coord = np.mean(reg_coord, 0)
    # cut_coords=reg_coord)
    plotting.plot_prob_atlas(tmp_list, title=uu, display_mode="mosaic")

# %% Visualising AAL in RSN
# TO DO: Connect RSN to labels, run loop


tmp_img = image.get_data(fname)

new_img = np.where(tmp_img, np.isin(
    tmp_img, np.array(aal.indices[-26:], dtype='int')), 0)

new_nii = image.new_img_like(fname, data=new_img)

plotting.plot_roi(new_nii,  display_mode="mosaic")

# %%


yeo = datasets.fetch_atlas_yeo_2011()
print(
    "Yeo atlas nifti image (3D) with 17 parcels and liberal mask "
    f" is located at: {yeo['thick_17']}"
)

data = datasets.fetch_development_fmri(n_subjects=10)

print(
    "Functional nifti images (4D, e.g., one subject) "
    f"are located at : {data.func[0]!r}"
)
print(
    "Counfound csv files (of same subject) are located "
    f"at : {data['confounds'][0]!r}"
)


# ConenctivityMeasure from Nilearn uses simple 'correlation' to compute
# connectivity matrices for all subjects in a list
connectome_measure = ConnectivityMeasure(kind="correlation")

# useful for plotting connectivity interactions on glass brain

# create masker using MultiNiftiLabelsMasker to extract functional data within
# atlas parcels from multiple subjects using parallelization to speed up the
# computation
masker = MultiNiftiLabelsMasker(
    labels_img=yeo["thick_17"],
    standardize="zscore_sample",
    memory="nilearn_cache",
    n_jobs=2,
)

# extract time series from all subjects
time_series = masker.fit_transform(data.func, confounds=data.confounds)

# calculate correlation matrices across subjects and display
correlation_matrices = connectome_measure.fit_transform(time_series)

# Mean correlation matrix across 10 subjects can be grabbed like this,
# using connectome measure object
mean_correlation_matrix = connectome_measure.mean_

# grab center coordinates for atlas labels
coordinates = plotting.find_parcellation_cut_coords(labels_img=yeo["thick_17"])

# plot connectome with 80% edge strength in the connectivity
plotting.plot_connectome(
    mean_correlation_matrix,
    coordinates,
    edge_threshold="80%",
    title="Yeo Atlas 17 thick (func)",
)

# %%

masker = MultiNiftiLabelsMasker(
    labels_img=aal.maps,
    standardize="zscore_sample",
    memory="nilearn_cache",
    n_jobs=2,
)

# extract time series from all subjects
time_series = masker.fit_transform(data.func, confounds=data.confounds)

# calculate correlation matrices across subjects and display
correlation_matrices = connectome_measure.fit_transform(time_series)

# Mean correlation matrix across 10 subjects can be grabbed like this,
# using connectome measure object
mean_correlation_matrix = connectome_measure.mean_

# grab center coordinates for atlas labels
coordinates = plotting.find_parcellation_cut_coords(labels_img=aal.maps)

# %%
# plot connectome with 80% edge strength in the connectivity
plotting.plot_connectome(
    mean_correlation_matrix,
    coordinates,
    edge_threshold=0.5,
    title="Yeo Atlas 17 thick (func)",
)

# %% # Plotting results of regression coeffs
# TO DO: Colour nodes by RSNs

tmp1 = np.load("test_numpy.npy")

# %%'

coordinates = plotting.find_probabilistic_atlas_cut_coords(msdl.maps)

# %%
tmp2 = tmp1.copy()
tmp2[tmp2 <= 0] = 0
plotting.plot_connectome(
    tmp2,
    coordinates,
    edge_threshold=0.01196427,
    title="Reg_coef, age pos", colorbar=True, edge_cmap=plt.cm.RdBu
)
tmp3 = tmp1.copy()
tmp3[tmp3 > 0] = 0
plotting.plot_connectome(
    tmp3,
    coordinates,
    edge_threshold=0.01196427,
    title="Reg_coef, age neg", colorbar=True, edge_cmap=plt.cm.RdBu
)
