from joblib import Parallel, delayed
from scipy.stats import entropy
import glob
import numpy as np
import nibabel as nib
import os

# Do entropy map
def perform_test_on_voxel(voxel_values):
    """
    Compute the entropy for a given voxel.
    The function first replace each element of the voxel-array with the corresponding probability.
    The new array is then passed to scipy.stats.entropy() function to compute and return a single entropy value.
    voxel_values = array of size equivalent to the total number segmentation results per subject where each element of the array represents the classification result from each segmentation file
    """
    prob = np.unique(voxel_values, return_counts=True)[1]/len(voxel_values)
    p = entropy(prob)
    return p

def entropy_voxel(directory, freesurfer):
    """
    directory = path to the directory where all segmentation results from a single subject are stored
    """
    if freesurfer:
        complete = os.listdir('entropy_maps/freesurfer')
        complete = [x.split('.')[0] for x in complete]

        subject = directory.split('/')[-1]
        if subject in complete: 
            print(f'Already done {subject}')
            return [0]

    # read and store all segmentation files loaded as 3D array into numpy arry
    files = glob.glob(os.path.join(directory, '*.mgz'))
    #if ([f for f in files if 'presurf_3' in f]):
    if freesurfer: files = files[:5]
    print(files)
    files = np.array([nib.load(f).get_fdata() for f in files])
    
    # size of the array = the number of segmentation result files
    total = len(files)
    print(total)
    print(files.shape)
    
    # prob_array represents the new 3D image built from segmented classes of the result image
    # Each voxel is represented by an array of x elements, where x = the total number of segmentation results
    # Each integer element of the array represents the brain region classified by FastSurfer's segmentation pipeline
    # Brain region corresponding to each integer value is found in the atlas above
     
    prob_array = np.zeros((256, 256, 256, total))
    for idx, f in enumerate(files):
        for i in range(256):
            for j in range(256):
                for k in range(256):
                    prob_array[i, j, k, idx] = int(f[i, j, k])

    print('Completed prob array')
    # Transform the result image (prob_array) into a 2D array where each element of the array represents a voxel
    # Each voxel = array of x elements containing the classified brain regions
    flattened_data = np.reshape(prob_array, (256*256*256, 5))
    
    print('Starting pvalues')
    # Execute perform_test_on_voxel to compute the entropy value of each voxel array
    p_values = Parallel(n_jobs=-1)(
        delayed(perform_test_on_voxel)(flattened_data[i])
        for i in range(flattened_data.shape[0])
    )

    # Reshape the results from p-values back into the shape of a single 3D voxel grid
    p_values = np.array(p_values).reshape((256,256,256))

    return p_values

for subject in os.listdir('/home/ines/Documents/Thesis/FreeSurfer/fs_seg'):
    if not 'sub' in subject: continue
    print(subject)
    result = entropy_voxel(f'/home/ines/Documents/Thesis/FreeSurfer/fs_seg/{subject}', freesurfer=True)
    if len(result) != 256: continue
    np.save(f'entropy_maps/freesurfer/{subject}.npy', result)

for subject in os.listdir('/home/ines/Documents/Thesis/FreeSurfer/fastsurfer_output_meshed'):
    if 'fs' in subject: continue
    print(subject)
    result = entropy_voxel(f'/home/ines/Documents/Thesis/FreeSurfer/fastsurfer_output_meshed/{subject}', freesurfer=False)
    np.save(f'entropy_maps/fastsurfer/{subject}.npy', result)

