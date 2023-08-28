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


# %% COBRE MSDL

msdl = datasets.fetch_atlas_msdl()
coordinates = plotting.find_probabilistic_atlas_cut_coords(msdl.maps)


# %% Make colours MSDL

# Find unique RSN labels
lbls_vec = np.array(msdl.networks)
unique_lbls = np.unique(lbls_vec)


c_range = np.arange(0 + 1e-5, 1-1e-5, step=1/len(unique_lbls))


cmaps = plt.cm.rainbow(c_range)

cmap_list = []
for k in range(cmaps.shape[0]):
    cmap_list.append(clrs.rgb2hex(cmaps[k, :]))

cmap_list = np.array(cmap_list, dtype="<U8")
node_cols = np.zeros(len(msdl.labels), dtype="<U8")

for j in range(len(unique_lbls)):
    for i in range(len(msdl.labels)):
        if msdl.networks[i] == unique_lbls[j]:
            node_cols[i] = cmap_list[j]


plt.figure()
plt.axis("off")
x = 0
k = 0
incr = int(len(unique_lbls)/3)
for i in range(len(unique_lbls)):
    if k > incr:
        k = 0
        x = x + 0.01
    k += 1
    plt.plot([x], [k], marker="o", color=cmaps[i])
    plt.text(x+0.001, k, unique_lbls[i], va="center")
plt.savefig("img/msdl_node_colours.png", dpi=900, bbox_inches="tight")
plt.close()

# %%

data_atlas = "COBRE MSDL"

preds = ["age", "groupPatient"]

reg_list = [f"data/cobre_{preds[0]}_coeffs.npy",
            f"data/cobre_{preds[1]}_coeffs.npy"]

for i in range(len(preds)):
    f = reg_list[i]
    B = np.load(f)
    thresh = np.quantile(np.abs(B), 0.0)  # only display top 10 %

    if preds[i] == "groupPatient":
        add_t = "Schizophrenic group"
    else:
        add_t = preds[i].title()

    B_neg = B.copy()
    B_neg[B_neg > 0] = 0
    fig, ax = plt.subplots()
    T1 = f"{data_atlas} negative regression coefficients\n" + add_t

    plt.title(T1)
    # plt.title(f"{data_atlas} negative regression coefficients\n{preds[i]}")
    p_neg = plotting.plot_connectome(adjacency_matrix=B_neg,
                                     node_coords=coordinates,
                                     edge_threshold=thresh,
                                     colorbar=True,
                                     node_color=node_cols,
                                     edge_cmap=plt.cm.RdBu,
                                     axes=ax,
                                     node_size=10,
                                     display_mode="xz")
    # plt.show()
    plt.savefig(f"img/{data_atlas}_{preds[i]}_negative.png", dpi=900)
    plt.close()

    B_pos = B.copy()
    B_pos[B_pos <= 0] = 0
    fig, ax = plt.subplots()
    T2 = f"{data_atlas} positive regression coefficients\n" + add_t
    plt.title(T2)
    # plt.title(f"{data_atlas} positive regression coefficients\n{preds[i]}")
    p_neg = plotting.plot_connectome(adjacency_matrix=B_pos,
                                     node_coords=coordinates,
                                     edge_threshold=thresh,
                                     colorbar=True,
                                     node_color=node_cols,
                                     edge_cmap=plt.cm.RdBu,
                                     axes=ax,
                                     node_size=10,
                                     display_mode="xz")
    # plt.show()
    plt.savefig(f"img/{data_atlas}_{preds[i]}_positive.png", dpi=900)
    plt.close()

# %% Make colours AAL


aal = datasets.fetch_atlas_aal()
coordinates = plotting.find_parcellation_cut_coords(aal.maps)
aal_rsn = pd.read_csv("data/aal_to_rsn.csv")

rsn_list = np.array(aal_rsn["rsn"])


# Find unique RSN labels
lbls_vec = np.array(rsn_list)
unique_lbls = np.unique(lbls_vec)

c_range = np.arange(0 + 1e-5, 1-1e-5, step=1/len(unique_lbls))

for j in range(len(c_range)):
    if c_range[j] > 0.7:
        c_range[j] += 0.1


cmaps = plt.cm.tab20(c_range)

cmap_list = []
for k in range(cmaps.shape[0]):
    cmap_list.append(clrs.rgb2hex(cmaps[k, :]))

cmap_list = np.array(cmap_list, dtype="<U8")
node_cols = np.zeros(len(rsn_list), dtype="<U8")

for j in range(len(unique_lbls)):
    for i in range(len(rsn_list)):
        if rsn_list[i] == unique_lbls[j]:
            node_cols[i] = cmap_list[j]


plt.figure()
plt.axis("off")
x = 0
k = 0
incr = int(len(unique_lbls)/3)
for i in range(len(unique_lbls)):
    if k > incr:
        k = 0
        x = x + 0.01
    k += 1
    plt.plot([x], [k], marker="o", color=cmaps[i])
    plt.text(x+0.001, k, unique_lbls[i], va="center")
# plt.show()
plt.savefig("img/aal_node_colours.png", dpi=900, bbox_inches="tight")
plt.close()

# %% COBRE AAL

data_atlas = "COBRE AAL"

preds = ["age", "groupPatient"]

reg_list = [f"data/cobre_aal_{preds[0]}_coeffs.npy",
            f"data/cobre_aal_{preds[1]}_coeffs.npy"]

for i in range(len(preds)):
    f = reg_list[i]
    B = np.load(f)
    thresh = np.quantile(np.abs(B[np.nonzero(B)]),
                         0.)  # only display top 10 %
    if preds[i] == "groupPatient":
        add_t = "Schizophrenic group"
    else:
        add_t = preds[i].title()
    B_neg = B.copy()
    B_neg[B_neg > 0] = 0
    fig, ax = plt.subplots()
    T1 = f"{data_atlas} negative regression coefficients\n" + add_t

    plt.title(T1)
    p_neg = plotting.plot_connectome(adjacency_matrix=B_neg,
                                     node_coords=coordinates,
                                     edge_threshold=thresh,
                                     colorbar=True,
                                     node_color=node_cols,
                                     edge_cmap=plt.cm.RdBu,
                                     axes=ax,
                                     node_size=10,
                                     display_mode="xz")
    # plt.show()
    plt.savefig(f"img/{data_atlas}_{preds[i]}_negative.png", dpi=900)
    plt.close()

    B_pos = B.copy()
    B_pos[B_pos <= 0] = 0
    fig, ax = plt.subplots()
    T2 = f"{data_atlas} positive regression coefficients\n" + add_t
    plt.title(T2)
    p_neg = plotting.plot_connectome(adjacency_matrix=B_pos,
                                     node_coords=coordinates,
                                     edge_threshold=thresh,
                                     colorbar=True,
                                     node_color=node_cols,
                                     edge_cmap=plt.cm.RdBu,
                                     axes=ax,
                                     node_size=10,
                                     display_mode="xz")
    # plt.show()
    plt.savefig(f"img/{data_atlas}_{preds[i]}_positive.png", dpi=900)
    plt.close()

# %% ABIDE

data_atlas = "ABIDE AAL"

preds = ["age", "groupAutism", "eyeClosed", "sexMale"]

reg_list = [f"data/abide_{preds[0]}_coeffs.npy",
            f"data/abide_{preds[1]}_coeffs.npy",
            f"data/abide_{preds[2]}_coeffs.npy",
            f"data/abide_{preds[3]}_coeffs.npy"
            ]

for i in range(len(preds)):
    f = reg_list[i]
    B = np.load(f)
    thresh = np.quantile(np.abs(B[np.nonzero(B)]),
                         0.)  # only display top 10 %

    B_neg = B.copy()
    B_neg[B_neg > 0] = 0

    if preds[i] == "groupAutism":
        add_t = "Autism spectrum disorder group"
    elif preds[i] == "eyeClosed":
        add_t = "Eyes closed group"
    elif preds[i] == "sexMale":
        add_t = "Male group"
    else:
        add_t = preds[i].title()

    fig, ax = plt.subplots()
    T1 = f"{data_atlas} negative regression coefficients\n" + add_t

    plt.title(T1)
    # plt.title(f"{data_atlas} negative regression coefficients\n{preds[i]}")
    p_neg = plotting.plot_connectome(adjacency_matrix=B_neg,
                                     node_coords=coordinates,
                                     edge_threshold=thresh,
                                     colorbar=True,
                                     node_color=node_cols,
                                     edge_cmap=plt.cm.RdBu,
                                     axes=ax,
                                     node_size=10,
                                     display_mode="xz")
    # plt.show()
    plt.savefig(f"img/{data_atlas}_{preds[i]}_negative.png", dpi=900)
    plt.close()

    B_pos = B.copy()
    B_pos[B_pos <= 0] = 0
    fig, ax = plt.subplots()
    T2 = f"{data_atlas} positive regression coefficients\n" + add_t
    plt.title(T2)
    # plt.title(f"{data_atlas} positive regression coefficients\n{preds[i]}")
    p_neg = plotting.plot_connectome(adjacency_matrix=B_pos,
                                     node_coords=coordinates,
                                     edge_threshold=thresh,
                                     colorbar=True,
                                     node_color=node_cols,
                                     edge_cmap=plt.cm.RdBu,
                                     axes=ax,
                                     node_size=10,
                                     display_mode="xz")
    # plt.show()
    plt.savefig(f"img/{data_atlas}_{preds[i]}_positive.png", dpi=900)
    plt.close()
