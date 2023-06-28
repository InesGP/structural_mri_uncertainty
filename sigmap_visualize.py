import os
import nibabel as nib
from nilearn import plotting
import numpy as np
import argparse

def visualize_reg(folder, savepath):

    subjects = os.listdir(f"{folder}")
    for subject in subjects:
        if not 'norm' in subject: continue
        
        img = nib.load(f"{folder}/{subject}/moved0.nii.gz")
        sig = np.load(f"{folder}/{subject}/nonlinear_fuzzy_reg.npy")

        img = nib.nifti1.Nifti1Image(sig, img.affine)
        subject = subject.split('norm-')[-1]

        if list(set(list(sig[sig != 0])))[0] == 23.:
            display = plotting.plot_img(img, cut_coords=(53,0,25), annotate=False, draw_cross=False, black_bg=True, threshold=0, bg_img=None,cmap='RdYlGn_r',colorbar=False) #, axes=axes[0])
        else:
            display = plotting.plot_img(img, cut_coords=(53,0,25), annotate=False, draw_cross=False, black_bg=True, threshold=0, bg_img=None,cmap='RdYlGn',colorbar=False, vmin=0, vmax=23) #, axes=axes[0])
        display.title(f"Non-Linearly Registered Image; Mean Significant Bit: {np.mean(sig[sig != 0]):.2f}", size=15)
        display.savefig(f"{savepath}/{subject}_sigmap.png")


def visualize_warp(folder, savepath):

    subjects = os.listdir(f"{folder}") 
    for subject in subjects:
        if not 'norm' in subject: continue

        img = nib.load(f"{folder}/{subject}/moved0.nii.gz")
        sig_x = np.load(f"{folder}/{subject}/nonlinear_fuzzy_0.npy")
        sig_y = np.load(f"{folder}/{subject}/nonlinear_fuzzy_1.npy")
        sig_z = np.load(f"{folder}/{subject}/nonlinear_fuzzy_2.npy")
        sig = ((sig_x + sig_y + sig_z)/3.)

        img = nib.nifti1.Nifti1Image(sig, img.affine)
        subject = subject.split('norm-')[-1]

        if list(set(list(sig[sig != 0])))[0] == 23.:
            display = plotting.plot_img(img, cut_coords=(64,-25,44), draw_cross=False, black_bg=True, threshold=0, bg_img=None,cmap='RdYlGn_r',colorbar=False) #, axes=axes[0])
        else:
            display = plotting.plot_img(img, cut_coords=(64,-25,44), draw_cross=False, black_bg=True, threshold=0, bg_img=None,cmap='RdYlGn',colorbar=False, vmin=0, vmax=23) #, axes=axes[0])
    #     display.title(f"Fuzzy Non-Linearly Registered {subject}\nMean Significant Digit: {np.mean(sig[sig != 0])}", size=10)
        display.title(f"Warp Field; Mean Significant Bit: {np.mean(sig[sig != 0]):.2f}", size=15)
        display.savefig(f"{savepath}/{subject}_sigmap.png")

#return means for boxplot
def warp_mean_sigdigs(folder, savepath):

    subjects = os.listdir(f"{folder}") 
    for subject in subjects:
        if not 'norm' in subject: continue


        sig_x = np.load(f"{folder}/{subject}/nonlinear_fuzzy_0.npy")
        sig_y = np.load(f"{folder}/{subject}/nonlinear_fuzzy_1.npy")
        sig_z = np.load(f"{folder}/{subject}/nonlinear_fuzzy_2.npy")
        sig = ((sig_x + sig_y + sig_z)/3.)

        subject = subject.split('norm-')[-1]
        print(f"'{subject}': {np.mean(sig[sig != 0])}")

#return means for boxplot
def reg_mean_sigdigs(folder, savepath):

    subjects = os.listdir(f"{folder}")
    for subject in subjects:
        if not 'norm' in subject: continue


        sig = np.load(f"{folder}/{subject}/nonlinear_fuzzy_reg.npy")
        
        subject = subject.split('norm-')[-1]
        print(f"'{subject}': {np.mean(sig[sig != 0])}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        ("Calculate significant digits for SynthMorph output")
    )

    parser.add_argument(
        "-f", "--folder", required=True, help=("Folder containing registered images"))
    parser.add_argument(
        "-s", "--savepath", required=True, help="path to folder where images are saved")
    parser.add_argument(
        "-w", "--warp", help="Use if the sigbits calculated is for warps", action="store_true")
    parser.add_argument(
        "-sd", "--sigdigs", help="Get mean sigdigs", action="store_true")

    args = parser.parse_args()

    if(args.warp):
        visualize_warp(folder=args.folder, savepath=args.savepath)
    elif (args.sigdigs):
        print('Registered Sigdigs')
        reg_mean_sigdigs(folder=args.folder, savepath=args.savepath)
        print('Warp Sigdigs')
        warp_mean_sigdigs(folder=args.folder, savepath=args.savepath)
    else:
        visualize_reg(folder=args.folder, savepath=args.savepath)

