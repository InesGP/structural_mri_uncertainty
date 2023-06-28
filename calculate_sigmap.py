import significantdigits
import os
import torchio as tio
import numpy as np
from significantdigits import Error, Method
import argparse
import brainload as bl

def calculate(folder, subject, ieee):

    t1s = []

    files = os.listdir(f"{folder}/{subject}")

    for f in files:
        if 'reg' in f: 
            img = tio.ScalarImage(f"{folder}/{subject}/{f}")
            t1s.append(img.data.numpy().squeeze())

    mean = np.array(t1s)

    mean = np.sum(mean, axis=0)/len(mean)

    np.save(f"{folder}/{subject}/mean_{subject}.npy", mean)

    
    if ieee:
        t1s = []

        files = os.listdir(f"{folder}/{subject}/ieee")

        for f in files:
            img = tio.ScalarImage(f"{folder}/{subject}/ieee/{f}")
            t1s.append(img.data.numpy().squeeze())


    sig = significantdigits.significant_digits(
            array=t1s,
            reference=mean,
            base=2,
            axis=0,
            error=Error.Relative,
            method=Method.General,
        )

    if ieee: np.save(f"{folder}/{subject}/ieee/nonlinear_ieee.npy", sig)
    else: np.save(f"{folder}/{subject}/nonlinear_fuzzy.npy", sig)

def calculate_warp(folder, subject):
    warp_x = []
    warp_y = []
    warp_z = []

    files = os.listdir(f"{folder}/{subject}")

    for f in files:
        if 'm3z' in f:
            print(f"{folder}/{subject}/{f}")
            warp = bl.freesurferdata.read_m3z_file(f"{folder}/{subject}/{f}")
            warp_x.append(warp[0])
            warp_y.append(warp[1])
            warp_z.append(warp[2])

    mean_x = np.array(warp_x)
    mean_x = np.sum(mean_x, axis=0)/len(mean_x)

    mean_y = np.array(warp_y)
    mean_y = np.sum(mean_y, axis=0)/len(mean_y)

    mean_z = np.array(warp_z)
    mean_z = np.sum(mean_z, axis=0)/len(mean_z)


    sig_x = significantdigits.significant_digits(
            array=warp_x,
            reference=mean_x,
            base=2,
            axis=0,
            error=Error.Relative,
            method=Method.General,
        )

    sig_y = significantdigits.significant_digits(
            array=warp_y,
            reference=mean_y,
            base=2,
            axis=0,
            error=Error.Relative,
            method=Method.General,
        )

    sig_z = significantdigits.significant_digits(
            array=warp_z,
            reference=mean_z,
            base=2,
            axis=0,
            error=Error.Relative,
            method=Method.General,
        )

    np.save(f"{folder}/{subject}/nonlinear_fuzzy_x.npy", sig_x)
    np.save(f"{folder}/{subject}/nonlinear_fuzzy_y.npy", sig_y)
    np.save(f"{folder}/{subject}/nonlinear_fuzzy_z.npy", sig_z)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(('Calculate significant digits for Freesurfer output'))

    parser.add_argument('-f', '--folder', required=True,
                        help=('Folder containing registered images'))
    parser.add_argument('-s', '--subject', required=True,
                        help='ID of the subject to use')
    parser.add_argument('-w', '--warp', action='store_true')
    parser.add_argument('--ieee', action='store_true',
                        help=('If set, IEEE significant digits are calculated'))
   
    args = parser.parse_args()
    
    if args.warp: calculate_warp(folder=args.folder, subject=args.subject)
    else: calculate(folder=args.folder, subject=args.subject, ieee=args.ieee)

