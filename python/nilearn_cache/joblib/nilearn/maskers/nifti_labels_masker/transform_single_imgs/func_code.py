# first line: 466
    def transform_single_imgs(self, imgs, confounds=None, sample_mask=None):
        """Extract signals from a single 4D niimg.

        Parameters
        ----------
        imgs : 3D/4D Niimg-like object
            See :ref:`extracting_data`.
            Images to process.
            If a 3D niimg is provided, a singleton dimension will be added to
            the output to represent the single scan in the niimg.

        confounds : CSV file or array-like or :obj:`pandas.DataFrame`, optional
            This parameter is passed to signal.clean. Please see the related
            documentation for details.
            shape: (number of scans, number of confounds)

        sample_mask : Any type compatible with numpy-array indexing, optional
            shape: (number of scans - number of volumes removed, )
            Masks the niimgs along time/fourth dimension to perform scrubbing
            (remove volumes with high motion) and/or non-steady-state volumes.
            This parameter is passed to signal.clean.

                .. versionadded:: 0.8.0

        Returns
        -------
        region_signals : 2D numpy.ndarray
            Signal for each label.
            shape: (number of scans, number of labels)

        Warns
        -----
        DeprecationWarning
            If a 3D niimg input is provided, the current behavior
            (adding a singleton dimension to produce a 2D array) is deprecated.
            Starting in version 0.12, a 1D array will be returned for 3D
            inputs.

        """
        # We handle the resampling of labels separately because the affine of
        # the labels image should not impact the extraction of the signal.

        if not hasattr(self, '_resampled_labels_img_'):
            self._resampled_labels_img_ = self.labels_img_

        if not hasattr(self, '_resampled_mask_img'):
            self._resampled_mask_img = self.mask_img_

        if self.resampling_target == "data":
            imgs_ = _utils.check_niimg(imgs, atleast_4d=True)
            if not _utils.niimg_conversions._check_same_fov(
                imgs_,
                self._resampled_labels_img_,
            ):
                if self.verbose > 0:
                    print("Resampling labels")
                labels_before_resampling = set(
                    np.unique(
                        _utils.niimg._safe_get_data(
                            self._resampled_labels_img_,
                        )
                    )
                )
                self._resampled_labels_img_ = self._cache(
                    image.resample_img, func_memory_level=2)(
                        self.labels_img_, interpolation="nearest",
                        target_shape=imgs_.shape[:3],
                        target_affine=imgs_.affine)
                labels_after_resampling = set(
                    np.unique(
                        _utils.niimg._safe_get_data(
                            self._resampled_labels_img_,
                        )
                    )
                )
                labels_diff = labels_before_resampling.difference(
                    labels_after_resampling
                )
                if len(labels_diff) > 0:
                    warnings.warn("After resampling the label image to the "
                                  "data image, the following labels were "
                                  f"removed: {labels_diff}. "
                                  "Label image only contains "
                                  f"{len(labels_after_resampling)} labels "
                                  "(including background).")

            if (self.mask_img is not None) and (
                not _utils.niimg_conversions._check_same_fov(
                    imgs_,
                    self._resampled_mask_img,
                )
            ):
                if self.verbose > 0:
                    print("Resampling mask")
                self._resampled_mask_img = self._cache(
                    image.resample_img, func_memory_level=2)(
                        self.mask_img_, interpolation="nearest",
                        target_shape=imgs_.shape[:3],
                        target_affine=imgs_.affine)

            # Remove imgs_ from memory before loading the same image
            # in filter_and_extract.
            del imgs_

        target_shape = None
        target_affine = None
        if self.resampling_target == 'labels':
            target_shape = self._resampled_labels_img_.shape[:3]
            target_affine = self._resampled_labels_img_.affine

        params = _utils.class_inspect.get_params(
            NiftiLabelsMasker,
            self,
            ignore=['resampling_target'],
        )
        params['target_shape'] = target_shape
        params['target_affine'] = target_affine
        params['clean_kwargs'] = self.clean_kwargs

        region_signals, labels_ = self._cache(
            _filter_and_extract,
            ignore=['verbose', 'memory', 'memory_level'],
        )(
            # Images
            imgs, _ExtractionFunctor(
                self._resampled_labels_img_,
                self.background_label,
                self.strategy,
                self._resampled_mask_img,
            ),
            # Pre-processing
            params,
            confounds=confounds,
            sample_mask=sample_mask,
            dtype=self.dtype,
            # Caching
            memory=self.memory,
            memory_level=self.memory_level,
            verbose=self.verbose,
        )

        self.labels_ = labels_

        return region_signals
