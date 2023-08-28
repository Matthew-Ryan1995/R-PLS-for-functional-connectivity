#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 11:18:30 2023

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
import pandas as pd

plt.rcParams["font.family"] = "Times New Roman"
# plt.rcParams["font.size"] = 6

# %% data

aal = datasets.fetch_atlas_aal()
fname = aal.maps
cmap = plt.cm.gist_ncar(np.linspace(0, 256, len(aal.labels) + 1))[1:]

aal_rsn = pd.read_csv("data/aal_to_rsn.csv")

rsn_list = np.array(aal_rsn["rsn"])

# %%


# Find unique RSN labels
lbls_vec = np.array(rsn_list)
unique_lbls = np.unique(lbls_vec)
# Get full AAL image
base_aal_img = image.get_data(fname)


# c_range = np.arange(0 + 1e-5, 1-1e-5, step=1/len(unique_lbls))
c_range = np.arange(0 + 1e-5, 1-1e-5, step=1/len(unique_lbls))

cmaps = list()

for j in c_range:
    if j > 0.7:
        j += 0.1
    # cmaps.append(clrs.ListedColormap(plt.cm.rainbow(j)))
    cmaps.append(clrs.ListedColormap(plt.cm.tab20(j)))
# %%
for i in range(len(unique_lbls)):
    # get labels for RSN
    idx = np.where(rsn_list == unique_lbls[i])[0]

    # Pull out only those labels
    new_img = np.where(base_aal_img,
                       np.isin(base_aal_img,
                               np.array(aal.indices,
                                        dtype='int')[idx]),
                       0)
    # Create new NII
    new_nii = image.new_img_like(fname, data=new_img)

    # Plot result
    plt.figure()

    pp = plotting.plot_roi(new_nii,
                           display_mode="mosaic",
                           cmap=cmaps[i],
                           # axes=ax,
                           axes=(0, 0, 0.5, 1),
                           # title=f"{unique_lbls[i]}"
                           )
    plt.title(f"{unique_lbls[i]}", size=22,  y=1, x=-3, color="white",
              bbox=dict(facecolor="white", color="black"))
    plt.savefig(f"img/aal_{unique_lbls[i]}.png", dpi=900, bbox_inches="tight")
    plt.close()
