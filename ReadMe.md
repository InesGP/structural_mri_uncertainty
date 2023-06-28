## README

* In order to determine the numerical uncertainty between FreeSurfer, SynthMorph and FastSurfer, first build Singularity containers from the Dockerfiles provided
* Freesurfer v7.3.1 without MCA were pulled directly from Dockerhub
* Freesurfer v7.3.1 with MCA was built using the Dockerhub image and [this Fuzzy script](https://github.com/verificarlo/fuzzy/blob/master/docker/resources/build_fuzzy_libmath_dockerfile.sh) which copies over the Fuzzy Libmath libraries
* FastSurfer and SynthMorph can be run in the same container with or without MCA by adding or removing the valgrind option
* [docker2singularity](https://github.com/singularityhub/docker2singularity) can be used to convert the Docker image to Singularity

#### FreeSurfer
Sample command for non-linear registration preprocessing:
```
singularity exec --writable-tmpfs -B INPUT_DIR:/root SINGULARITY_IMAGE \
	recon-all -verbose -sd /root -subjid sub-01 \
	-log logging.log -status status.log \
	-motioncor \
	-talairach \
	-nuintensitycor \
	-normalization \
	-skullstrip \
	-gcareg \
	-canorm
```
Sample command for non-linear registration:
```
singularity exec --writable-tmpfs -B INPUT_DIR:/root SINGULARITY_IMAGE \
	recon-all -verbose -sd /root -subjid sub-01 \
	-log logging.log -status status.log \
	-careg
``` 
* The instrumentation for FreeSurfer originates from the libraries compiled with Verificarlo, no additional commands are needed besides calling the container with FreeSurfer and MCA

Sample command for whole brain segmentation:
```
singularity exec --writable-tmpfs -B INPUT_DIR:/root SINGULARITY_IMAGE \
	recon-all -verbose -sd /root -subjid sub-01 \
	-log logging.log -status status.log \
	-motioncor \
	-talairach \
	-nuintensitycor \
	-normalization \
	-skullstrip \
	-gcareg \
	-canorm \
	-careg \
	-calabel
```
* More information about FreeSurfer recon-all is available [here](https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all#CARegister.28-.3Cno.3Ecareg.29)

##### To better understand the SynthMorph and FastSurfer Verrou commands, consult the [Verrou documentation](https://edf-hpc.github.io/verrou/vr-manual.html)
#### SynthMorph

Sample command for non-linear registration without Verrou:
```
singularity exec --writable-tmpfs \
      -B results:/voxelmorph/nifty\
      -B scans:/voxelmorph/scans\
      SINGULARITY_IMAGE valgrind --tool=verrou --exclude=/voxelmorph/libm.tex --instr-atstart=no\
      python3 /voxelmorph/scripts/tf/register.py --moving /voxelmorph/scans/sub-01.nii.gz \
      --fixed /voxelmorph/data/norm-average_mni305.mgz --model /voxelmorph/data/brains-dice-vel-0.5-res-16-256f.h5\
      --moved /voxelmorph/nifty/moved_sub-01.nii.gz --warp /voxelmorph/nifty/warp_sub-01.nii.gz
```

Sample command for non-linear registration with Verrou:
```
singularity exec --writable-tmpfs --env VERROU_LIBM_ROUNDING_MODE=random --env VERROU_ROUNDING_MODE=random --env LD_PRELOAD=/voxelmorph/interlibmath.so\
      -B OUTPUT_DIR:/voxelmorph/nifty\
      -B INPUT_DIR:/voxelmorph/scans\
      SINGULARITY_IMAGE valgrind --tool=verrou --exclude=/voxelmorph/libm.tex --instr-atstart=no\
      python3 /voxelmorph/scripts/tf/register.py --moving /voxelmorph/scans/sub-01.nii.gz \
      --fixed /voxelmorph/data/norm-average_mni305.mgz --model /voxelmorph/data/brains-dice-vel-0.5-res-16-256f.h5\
      --moved /voxelmorph/nifty/moved_sub-01.nii.gz --warp /voxelmorph/nifty/warp_sub-01.nii.gz
```

#### FastSurfer
```
singularity exec --nv -B INPUT_DIR:/data \
	-B OUTPUT_DIR:/output \
	-B LICENSE_DIR:/fs_license \
	SINGULARITY_IMAGE \
	/bin/bash -c "cd /home/valgrind-3.21.0+verrou-dev && \
	VERROU_LIBM_ROUNDING_MODE=random VERROU_ROUNDING_MODE=random LD_PRELOAD=/home/valgrind-3.21.0+verrou-dev/verrou/Interlibmath/interlibmath.so valgrind --tool=verrou --rounding-mode=random --exclude=/tmp/libm.ex --trace-children=yes \
	fastsurfer/run_fastsurfer.sh --t1 /data/$FILENAME --sid "sub-01" --sd /output --fs_license /fs_license/license.txt --seg_only --parallel --device cpu
```

