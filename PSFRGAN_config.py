config = {
    'gpus': 0,
    'seed': 23423,
    'name': 'experiment_name',
    'suffix': '',
    'checkpoints_dir': './check_points',
    'model': 'enhance',
    'input_nc': 3,
    'Dinput_nc': 3,
    'output_nc': 3,
    'ngf': 64,
    'ndf': 64,
    'n_layers_D': 4,
    'D_num': 3,
    'Pnorm': 'bn',
    'Gnorm': 'spade',
    'Dnorm': 'in',
    'init_type': 'normal',
    'init_gain': 0.02,
    'dataset_name': 'single',
    'Pimg_size': '512',
    'Gin_size': '512',
    'Gout_size': '512',
    'num_threads': 8,
    'batch_size': 16,
    'load_size': 512,
    'crop_size': 256,
    'max_dataset_size': float("inf"),
    'preprocess': 'none',
    'epoch': 'latest',
    'load_iter': '0',

}
