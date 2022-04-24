import matplotlib.pyplot as plt
from needlet_filters import *
from box_funcs import *

import matplotlib.patches as patches


''' 
Some preliminary testing of filter functions on 21cmfast box
'''

box = load_21cmfast("../boxes/delta_T_v3_z006.50_nf0.096743_useTs0_200_300Mpc")
box_slice = box[0]

Fourier = FourierSpace(box_slice)
fourier_grid = Fourier.grid_dimless()

kmax = 200 #max dimless k number == length of box in pixels
js = np.arange(1,5)

B1 = 4
B2= 2

Need1 = NeedletFilters(js, B= B1, kmax=kmax)
Need2 = NeedletFilters(js, B= B2, kmax=kmax)

filter_1d = False
if filter_1d:

    filters1 = Need1.needlet_filters_1d()
    filters2 = Need2.needlet_filters_1d()

    fig, ax = plt.subplots(nrows=1,ncols=2, figsize = (8.5,4))

    for f in filters1:
        ax[1].plot(np.arange(201),f)

    for i,f in enumerate(filters2):
        ax[0].plot(np.arange(201),f, label = f"j = {i+1}")

    rect1 = patches.Rectangle((B1, 0), 200, 200, linewidth=1, edgecolor='None', facecolor='0.8')
    ax[1].add_patch(rect1)

    rect2 = patches.Rectangle((B2, 0), 200, 200, linewidth=1, edgecolor='None', facecolor='0.8')
    ax[0].add_patch(rect2)


    ax[1].plot(np.arange(201),np.sum(filters1**2, axis=0), color = "k")
    ax[0].plot(np.arange(201),np.sum(filters2**2, axis=0), color = "k", label=r"$\Sigma \ b^2$")



    ax[0].set_title(f"$B$ = {B2}")
    ax[0].set_ylim(0,1.2)
    ax[0].set_xscale("log")  
    ax[0].set_xlim(1,200)
    ax[0].legend()
    ax[0].set_xlabel("$k$ [dimensionless]")
    ax[0].set_ylabel("$b(k,B,j)$")

    ax[1].set_title(f"$B$ = {B1}")
    ax[1].set_ylim(0,1.2)
    ax[1].set_xscale("log")
    ax[1].set_xlim(1,200)
    ax[1].set_xlabel("$k$ [dimensionless]")
    ax[1].set_ylabel("$b(k,B,j)$")

    plt.savefig("figures/needlet_filters.png", bbox_inches = "tight")
    # plt.savefig("docs/april2022/figures/needlet_filters.pdf", bbox_inches = "tight")


filter_2d = False

if filter_2d:
    filters = []
    filtered = []

    for j in js:
        filters_2d = Need1.needlet_filters_2d(j, fourier_grid)
        filters.append(filters_2d)

        filtered_box = Need1.filter_box(box_slice,j)
        filtered.append(filtered_box)


    fig, ax = plt.subplots(figsize = (8.5,4), nrows = 2,ncols=5)


    ax[0,0].imshow(box_slice)
    ax[0,0].set_xticklabels([])
    ax[0,0].set_yticklabels([])

    plt.subplots_adjust(wspace=0.2)

    for i in range(4):
        ax[0,i+1].imshow(filters[i])
        ax[0,i+1].set_xticklabels([])
        ax[0,i+1].set_yticklabels([])

        ax[0,i+1].tick_params(color=f'C{i}', labelcolor=f'C{i}')
        for spine in ax[0,i+1].spines.values():
            spine.set_edgecolor(f'C{i}')
            spine.set_linewidth(3)

    for i in range(4):
        ax[1,i+1].imshow(np.real(filtered[i]))
        ax[1,i+1].set_xticklabels([])
        ax[1,i+1].set_yticklabels([])

        ax[1,i+1].tick_params(color=f'C{i}', labelcolor=f'C{i}')
        for spine in ax[1,i+1].spines.values():
            spine.set_edgecolor(f'C{i}')
            spine.set_linewidth(3)

    filters1 = Need1.needlet_filters_1d()
    for f in filters1:
        ax[1,0].plot(np.arange(201),f)

    ax[1,0].set_xscale("log")
    ax[1,0].set_xlabel("$k$ [dimensionless]")
    ax[1,0].set_ylabel("$b(k,B,j)$")

    plt.savefig("figures/filtered_example.png", bbox_inches = "tight")
    # plt.savefig("docs/april2022/figures/filtered_example.pdf", bbox_inches = "tight")
