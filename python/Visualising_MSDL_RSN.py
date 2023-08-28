#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 11:02:24 2023

@author: rya200
"""

# %% Packages

from nilearn.maskers import MultiNiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure
from nilearn.maskers import NiftiMasker
from nilearn import datasets
from nilearn import plotting
from nilearn.regions import connected_label_regions
from nilearn import image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clrs

plt.rcParams["font.family"] = "Times New Roman"

# %% data

msdl = datasets.fetch_atlas_msdl()
# cmap = plt.cm.gist_ncar(np.linspace(0, 256, len(aal.labels) + 1))[1:]

img = image.load_img(msdl.maps)

lbls_vec = np.array(msdl.networks)
unique_lbls = np.unique(lbls_vec)


c_range = np.arange(0 + 1e-5, 1-1e-5, step=1/len(unique_lbls))
cmaps = list()
for j in c_range:
    cmaps.append(clrs.ListedColormap(plt.cm.rainbow(j)))
# cmaps = plt.cm.rainbow(c_range)

# cmap_list = []
# for k in range(cmaps.shape[0]):
#     cmap_list.append(clrs.rgb2hex(cmaps[k, :]))

# cmap_list = np.array(cmap_list, dtype="<U8")
# node_cols = np.zeros(len(msdl.labels), dtype="<U8")

# %% Visualising MSDL in RSN

# Find unique RSN labels
lbls_vec = np.array(msdl.networks)
unique_lbls = np.unique(lbls_vec)

for uu in unique_lbls:
    rsn_list = list()
    reg_coord = list()
    for i in np.where(lbls_vec == uu)[0]:  # Get all nodes in RSN
        rsn_list.append(image.index_img(img, i))
        reg_coord.append(msdl.region_coords[i])
    # reg_coord = np.array(reg_coord)
    idx = np.where(unique_lbls == uu)[0][0]

    reg_coord = plotting.find_probabilistic_atlas_cut_coords(rsn_list)
    reg_coord = np.mean(reg_coord, 0)
    # cut_coords=reg_coord)
    plt.figure()
    pp = plotting.plot_prob_atlas(rsn_list,  # Plot RSN nodes
                                  # title=uu,
                                  display_mode="mosaic",
                                  axes=(0, 0, 0.5, 1),
                                  cmap=cmaps[idx]
                                  # output_file=f"img/msdl_{uu}.png"
                                  )
    plt.title(uu, size=22,  y=1, x=-3, color="white",
              bbox=dict(facecolor="white", color="black"))
    # pp.savefig(f"img/msdl_{uu}.png", dpi=900)  # Save file
    plt.savefig(f"img/msdl_{uu}.png", dpi=900, bbox_inches="tight")
    plt.close()
