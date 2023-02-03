import pytest
import numpy as np
from matchms import Spectrum, calculate_scores
from matchms.networking import SimilarityNetwork
from matchms.similarity import FingerprintSimilarity
from matchmsextras.networking import create_network_asymmetric
from matchmsextras.networking import dilate_cluster
from matchmsextras.networking import extract_networking_metadata


def create_dummy_spectrum():
    """Create dummy spectrums"""
    fingerprints1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1]]
    fingerprints2 = [[1, 0, 1], [0, 1, 1], [1, 1, 1]]
    references = []
    queries = []
    for i, fp in enumerate(fingerprints1):
        references.append(Spectrum(mz=np.array([100, 200.]),
                                   intensities=np.array([0.7, 0.2]),
                                   metadata={"spectrumid": 'ref_spec_'+str(i),
                                             "fingerprint": np.array(fp),
                                             "smiles": 'C1=CC=C2C(=C1)NC(=N2)C3=CC=CO3',
                                             "parent_mass": 100+50*i}))
    for i, fp in enumerate(fingerprints2):
        queries.append(Spectrum(mz=np.array([100, 200.]),
                                intensities=np.array([0.7, 0.2]),
                                metadata={"spectrumid": 'query_spec_'+str(i),
                                          "fingerprint": np.array(fp),
                                          "smiles": 'CC1=C(C=C(C=C1)NC(=O)N(C)C)Cl',
                                          "parent_mass": 110+50*i}))
    return references, queries


def create_dummy_scores():
    references, queries = create_dummy_spectrum()

    # Create Scores object by calculating dice scores
    similarity_measure = FingerprintSimilarity("dice")
    scores = calculate_scores(references, queries, similarity_measure)
    return scores


def create_dummy_scores_symmetric():
    references, queries = create_dummy_spectrum()
    spectrums = references + queries

    # Create Scores object by calculating dice scores
    similarity_measure = FingerprintSimilarity("dice")
    scores = calculate_scores(spectrums, spectrums, similarity_measure)
    return scores


@pytest.fixture()
def network_symmetric():
    """Test creating a graph from a symmetric Scores object"""
    cutoff = 0.7
    scores = create_dummy_scores_symmetric()
    msnet = SimilarityNetwork(score_cutoff=cutoff)
    msnet.create_network(scores)
    return msnet.graph


def test_create_network_asymmetric():
    """Test creating a graph from a non-symmetric Scores object"""
    cutoff=0.7
    scores = create_dummy_scores()
    msnet = create_network_asymmetric(scores, cutoff=cutoff)
    nodes_list = list(msnet.nodes())
    nodes_list.sort()
    expected_nodes = ['query_spec_0', 'query_spec_1', 'query_spec_2',
                      'ref_spec_0', 'ref_spec_1', 'ref_spec_2',
                      'ref_spec_3', 'ref_spec_4']
    assert nodes_list == expected_nodes, "Expected different nodes in graph"

    edges_list = list(msnet.edges())
    edges_list.sort()
    nodes_with_edges = ['query_spec_0',
                        'query_spec_2',
                        'query_spec_2',
                        'ref_spec_3',
                        'ref_spec_4',
                        'ref_spec_4']
    assert len(edges_list) == np.sum(scores.scores.to_array() > cutoff), \
        "Expected different number of edges"
    assert np.all([(x[0] in nodes_with_edges) for x in edges_list]), "Expected different edges in graph"
    assert np.all([(x[1] in nodes_with_edges) for x in edges_list]), "Expected different edges in graph"
    assert msnet.get_edge_data('ref_spec_4', 'query_spec_0')["weight"] == 1, \
        "Expected different edge weight"
    assert msnet.get_edge_data('ref_spec_3', 'query_spec_2')["weight"] == 0.8, \
        "Expected different edge weight"


def test_dilate_cluster(network_symmetric):
    scores = create_dummy_scores_symmetric()
    assert len(network_symmetric.edges()) == 5, \
        "Expected different number of edges before dilating"

    # Dilation step
    msnet_dilated, _ = dilate_cluster(network_symmetric, scores)
    assert len(msnet_dilated.edges()) == 12, \
        "Expected different number of edges after dilating"


def test_extract_networking_metadata():
    references, queries = create_dummy_spectrum()
    spectrums = references + queries

    metadata = extract_networking_metadata(spectrums)
    assert metadata.shape == (8, 3), "Expected different shape of table"
    assert metadata.columns.to_list() == ['smiles', 'compound_name', 'parent_mass'], \
        "Expected different columns"
    assert metadata["parent_mass"].to_list() == [100, 150, 200, 250, 300, 110, 160, 210], \
        "Expected different parent masses"
