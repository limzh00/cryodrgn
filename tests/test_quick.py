import os.path
import argparse
import pytest
from cryodrgn.commands import train_vae, analyze, analyze_landscape, graph_traversal, eval_vol


DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'testing', 'data')


@pytest.fixture
def mrcs_file():
    return f'{DATA_FOLDER}/hand.mrcs'


@pytest.fixture
def poses_file():
    return f'{DATA_FOLDER}/hand_rot.pkl'


def test_run(mrcs_file, poses_file):
    args = train_vae.add_args(argparse.ArgumentParser()).parse_args([
        mrcs_file,
        '-o', 'output',
        '--lr', '.0001',
        '--num-epochs', '20',
        '--seed', '0',
        '--poses', poses_file,
        '--zdim', '10',
        '--pe-type', 'gaussian',
    ])
    train_vae.main(args)

    args = analyze.add_args(argparse.ArgumentParser()).parse_args([
        'output',
        '19',                     # Epoch number to analyze - 0-indexed
        '--pc', '3',              # Number of principal component traversals to generate
        '--ksample', '14',        # Number of kmeans samples to generate
        '--device', '0',
        '--vol-start-index', '1'
    ])
    analyze.main(args)

    args = analyze_landscape.add_args(argparse.ArgumentParser()).parse_args([
        'output',
        '19',                     # Epoch number to analyze - 0-indexed
        '--device', '0',
        '--sketch-size', '10',    # Number of volumes to generate for analysis
        '--downsample', '64',
        '--pc-dim', '5',
        '--vol-start-index', '1'
    ])
    analyze_landscape.main(args)

    args = graph_traversal.add_args(argparse.ArgumentParser()).parse_args([
        'output/z.19.pkl',
        '--anchors', '22', '49', '53', '6', '27', '95', '64', '81', '44', '58', '75', '67', '9', '89',
        '-o', 'output/graph_traversal_path.txt',
        '--out-z', 'output/graph_traversal_zpath.txt'
    ])
    graph_traversal.main(args)

    args = eval_vol.add_args(argparse.ArgumentParser()).parse_args([
        'output/weights.19.pkl',
        '--config', 'output/config.pkl',
        '--zfile', 'output/graph_traversal_zpath.txt',
        '-o', 'output/eval_vols'
    ])
    eval_vol.main(args)
