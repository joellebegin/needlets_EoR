from foreground_funcs import get_gsm_slice
import numpy as np
from box_funcs import *
from needlet_filters import *
import matplotlib.pyplot as plt
from tqdm import tqdm

box = load_21cmfast("../boxes/delta_T_v3_z006.50_nf0.096743_useTs0_200_300Mpc")
box_slice = box[0]
boxObj = Box(box_slice, z = 6.5)
box_freq = boxObj.nu_obs()
print(box_freq)
gsm_slice = get_gsm_slice(box_freq, np.array([45.,45.]), np.array([14.,14.]), sanity_check=True, plot_max = 8000)

added = gsm_slice+box_slice*1e-3
# plt.imshow(added)
# plt.show()

plot_boxes=False
if plot_boxes:
    fig, ax = plt.subplots(nrows = 1, ncols=2)
    plt.subplots_adjust(wspace = 0.4)
    im1=ax[0].imshow(gsm_slice)
    cbar1 = plt.colorbar(im1, ax = ax[0],fraction=0.046, pad=0.04)
    cbar1.set_label("Temp [K]")
    ax[0].set_yticks([])
    ax[0].set_xticks([])

    im2=ax[1].imshow(box_slice)
    cbar2 = plt.colorbar(im2, ax = ax[1],fraction=0.046, pad=0.04)
    cbar2.set_label("Temp [mK]")
    ax[1].set_yticks([])
    ax[1].set_xticks([])

    plt.savefig("fgnds_and_21cm.png", bbox_inches="tight")
    plt.savefig("../docs/april2022/figures/fgnds_and_21cm.pdf", bbox_inches="tight")


kmax = 200 #max dimless k number == length of box in pixels
js = np.arange(1,5)
B1 = 4
Need1 = NeedletFilters(js, B= B1, kmax=kmax)


filtered_fgnds = []
filtered_21cm = []

for j in tqdm(js):
    filtered_box = Need1.filter_box(gsm_slice,j)
    filtered_fgnds.append(np.real(filtered_box))

    filtered_box = Need1.filter_box(box_slice,j)
    filtered_21cm.append(np.real(filtered_box))


from matplotlib.colors import SymLogNorm



nrow = 2
ncol=5
fig, ax = plt.subplots(figsize = (8.5,4), nrows = 2,ncols=5, gridspec_kw=dict(wspace=0.5, hspace=0.0,
                     top=1. - 0.5 / (nrow + 1), bottom=0.5 / (nrow + 1),
                     left=0.5 / (ncol + 1), right=1 - 0.5 / (ncol + 1)))


im1 = ax[0,0].imshow(gsm_slice)
ax[0,0].set_xticklabels([])
ax[0,0].set_yticklabels([])
cbar1 = plt.colorbar(im1, ax = ax[0,0],fraction=0.046, pad=0.04)


im2 = ax[1,0].imshow(box_slice)
ax[1,0].set_xticklabels([])
ax[1,0].set_yticklabels([])
cbar1 = plt.colorbar(im2, ax = ax[1,0],fraction=0.046, pad=0.04)


plt.subplots_adjust(wspace=0.6,hspace=0)

ims = []
ims2 = []
cbars = []
for i in range(4):
    
    norm = SymLogNorm(1,vmin=np.min(filtered_fgnds[i]),vmax=np.max(filtered_fgnds[i]))
    ims.append(ax[0,i+1].imshow(filtered_fgnds[i],cmap = plt.cm.RdBu, norm=norm))
    ax[0,i+1].set_xticklabels([])
    ax[0,i+1].set_yticklabels([])

    
    ax[0,i+1].tick_params(color=f'C{i}', labelcolor=f'C{i}')
    for spine in ax[0,i+1].spines.values():
        spine.set_edgecolor(f'C{i}')
        spine.set_linewidth(3)

    norm = SymLogNorm(1,vmin=np.min(filtered_21cm[i]),vmax=np.max(filtered_21cm[i]))
    ims2.append(ax[1,i+1].imshow(filtered_21cm[i],cmap = plt.cm.RdBu, norm=norm))
    ax[1,i+1].set_xticklabels([])
    ax[1,i+1].set_yticklabels([])

    
    ax[1,i+1].tick_params(color=f'C{i}', labelcolor=f'C{i}')
    for spine in ax[1,i+1].spines.values():
        spine.set_edgecolor(f'C{i}')
        spine.set_linewidth(3)

    

for i in range(4):
    plt.colorbar(ims[i], ax = ax[0,i+1],fraction=0.046, pad=0.04)
    plt.colorbar(ims2[i], ax = ax[1,i+1],fraction=0.046, pad=0.04)

plt.savefig("figures/filtered_fgnds.png", bbox_inches = "tight")
plt.savefig("../docs/april2022/figures/filtered_fgnds.pdf", bbox_inches = "tight")