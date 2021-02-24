import pytest
import numpy as np
from matchms import Spectrum, calculate_scores
from matchms.similarity import FingerprintSimilarity
from matchms_extras.networking import create_network, create_network_asymmetric
from matchms_extras.networking import get_top_hits
from matchms_extras.networking import dilate_cluster
from matchms_extras.networking import extract_networking_metadata


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


def test_get_top_hits_by_references():
    scores = create_dummy_scores()
    idx_ref, scores_ref = get_top_hits(scores, top_n=10, search_by="references")

    expected_scores_ref = {'ref_spec_0': np.array([0.66666667, 0.5       , 0.        ]),
                           'ref_spec_1': np.array([0.66666667, 0.5       , 0.        ]),
                           'ref_spec_2': np.array([0.66666667, 0.66666667, 0.5       ]),
                           'ref_spec_3': np.array([0.8, 0.5, 0.5]),
                           'ref_spec_4': np.array([1. , 0.8, 0.5])}
    expected_idx_ref = {'ref_spec_0': np.array([0, 2, 1], dtype=np.int64),
                        'ref_spec_1': np.array([1, 2, 0], dtype=np.int64),
                        'ref_spec_2': np.array([1, 0, 2], dtype=np.int64),
                        'ref_spec_3': np.array([2, 1, 0], dtype=np.int64),
                        'ref_spec_4': np.array([0, 2, 1], dtype=np.int64)}
    for key in scores_ref.keys():
        assert np.allclose(scores_ref[key], expected_scores_ref[key], atol=1e-5), \
            "Expected different selected scores"
    for key in idx_ref.keys():
        assert np.allclose(idx_ref[key], expected_idx_ref[key], atol=1e-5), \
            "Expected different selected indices"

    # Test lower top_n
    idx_ref, scores_ref = get_top_hits(scores, top_n=2, search_by="references")
    for key in scores_ref.keys():
        assert np.allclose(scores_ref[key], expected_scores_ref[key][:2], atol=1e-5), \
            "Expected different selected scores"
    for key in idx_ref.keys():
        assert np.allclose(idx_ref[key], expected_idx_ref[key][:2], atol=1e-5), \
            "Expected different selected indices"

def test_get_top_hits_by_queries():
    scores = create_dummy_scores()
    idx_query, scores_query = get_top_hits(scores, top_n=10, search_by="queries")

    expected_scores_query = {'query_spec_0': np.array([1.        , 0.66666667, 0.66666667, 0.5       , 0.        ]),
                             'query_spec_1': np.array([0.66666667, 0.66666667, 0.5       , 0.5       , 0.        ]),
                             'query_spec_2': np.array([0.8, 0.8, 0.5, 0.5, 0.5])}
    expected_idx_query = {'query_spec_0': np.array([4, 2, 0, 3, 1], dtype=np.int64),
                          'query_spec_1': np.array([2, 1, 4, 3, 0], dtype=np.int64),
                          'query_spec_2': np.array([4, 3, 2, 1, 0], dtype=np.int64)}
    for key in scores_query.keys():
        assert np.allclose(scores_query[key], expected_scores_query[key], atol=1e-5), \
            "Expected different selected scores"
    for key in idx_query.keys():
        assert np.allclose(idx_query[key], expected_idx_query[key], atol=1e-5), \
            "Expected different selected indices"

    # Test lower top_n
    idx_query, scores_query = get_top_hits(scores, top_n=2, search_by="queries")
    for key in scores_query.keys():
        assert np.allclose(scores_query[key], expected_scores_query[key][:2], atol=1e-5), \
            "Expected different selected scores"
    for key in idx_query.keys():
        assert np.allclose(idx_query[key], expected_idx_query[key][:2], atol=1e-5), \
            "Expected different selected indices"


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
    assert len(edges_list) == np.sum(scores.scores > cutoff), \
        "Expected different number of edges"
    assert np.all([(x[0] in nodes_with_edges) for x in edges_list]), "Expected different edges in graph"
    assert np.all([(x[1] in nodes_with_edges) for x in edges_list]), "Expected different edges in graph"
    assert msnet.get_edge_data('ref_spec_4', 'query_spec_0')["weight"] == 1, \
        "Expected different edge weight"
    assert msnet.get_edge_data('ref_spec_3', 'query_spec_2')["weight"] == 0.8, \
        "Expected different edge weight"


def test_create_network_symmetric_wrong_input():
    """Test if function is used with non-symmetric scores object"""
    scores = create_dummy_scores()
    with pytest.raises(AssertionError) as msg:
        _ = create_network(scores)

    expected_msg = "Expected symmetric scores object with queries==references"
    assert expected_msg in str(msg), "Expected different exception"


def test_create_network_symmetric():
    """Test creating a graph from a symmetric Scores object"""
    cutoff=0.7
    scores = create_dummy_scores_symmetric()
    msnet = create_network(scores, cutoff=cutoff)

    edges_list = list(msnet.edges())
    edges_list.sort()
    nodes_without_edges = ['ref_spec_0',
                           'ref_spec_1',
                           'ref_spec_2']
    assert len(edges_list) == 5, "Expected different number of edges"
    assert np.all([(x[0] not in nodes_without_edges) for x in edges_list]), \
        "Expected this node to have no edges"
    assert np.all([(x[1] not in nodes_without_edges) for x in edges_list]), \
        "Expected this node to have no edges"


def test_create_network_symmetric_higher_cutoff():
    cutoff=0.9
    scores = create_dummy_scores_symmetric()
    msnet = create_network(scores, cutoff=cutoff)

    edges_list = list(msnet.edges())
    edges_list.sort()
    assert len(edges_list) == 1, "Expected only one link"
    assert edges_list[0][0] in ['query_spec_0', 'ref_spec_4'], \
        "Expected different node to have a link"
    assert edges_list[0][1] in ['query_spec_0', 'ref_spec_4'], \
        "Expected different node to have a link"


def test_create_network_symmetric_mutual_method():
    """Test creating a graph from a Scores object"""
    cutoff=0.7
    scores = create_dummy_scores_symmetric()
    # change some scores
    scores._scores[7, 6] = scores._scores[6, 7] = 0.85
    scores._scores[7, 5] = scores._scores[5, 7] = 0.75
    scores._scores[7, 3] = scores._scores[3, 7] = 0.7

    msnet = create_network(scores, cutoff=cutoff, top_n=3,
                           max_links=3, link_method="mutual")
    nodes_with_edges = ['query_spec_0', 'query_spec_1', 'query_spec_2', 'ref_spec_4']
    edges_list = list(msnet.edges())
    edges_list.sort()
    assert len(edges_list) == 3, "Expected only four link"
    assert np.all([(x[0] in nodes_with_edges) for x in edges_list]), "Expected different edges in graph"
    assert np.all([(x[1] in nodes_with_edges) for x in edges_list]), "Expected different edges in graph"


def test_create_network_symmetric_max_links_1():
    """Test creating a graph from a Scores object using max_links=1"""
    cutoff=0.7
    scores = create_dummy_scores_symmetric()
    msnet = create_network(scores, cutoff=cutoff, max_links=1, link_method="single")

    edges_list = list(msnet.edges())
    edges_list.sort()
    nodes_without_edges = ['ref_spec_0',
                           'ref_spec_1',
                           'ref_spec_2',]
    assert len(edges_list) == 3, "Expected different number of edges"
    assert np.all([(x[0] not in nodes_without_edges) for x in edges_list]), \
        "Expected this node to have no edges"
    assert np.all([(x[1] not in nodes_without_edges) for x in edges_list]), \
        "Expected this node to have no edges"


def test_dilate_cluster():
    # Create graph
    cutoff=0.7
    scores = create_dummy_scores_symmetric()
    msnet = create_network(scores, cutoff=cutoff, top_n=3, max_links=3)
    assert len(msnet.edges()) == 5, \
        "Expected different number of edges before dilating"

    # Dilation step
    msnet_dilated, links_added = dilate_cluster(msnet, scores)
    assert len(msnet.edges()) == 12, \
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
