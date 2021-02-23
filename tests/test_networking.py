import pytest
import numpy as np
from matchms import Spectrum, calculate_scores
from matchms.similarity import FingerprintSimilarity
from matchms_extras.networking import create_network, get_top_hits


def create_dummy_scores():
    # Create dummy spectrums
    fingerprints1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1]]
    fingerprints2 = [[1, 0, 1], [0, 1, 1], [1, 1, 1]]
    references = []
    queries = []
    for i, fp in enumerate(fingerprints1):
        references.append(Spectrum(mz=np.array([100, 200.]),
                                   intensities=np.array([0.7, 0.2]),
                                   metadata={"spectrumid": 'ref_spec_'+str(i),
                                             "fingerprint": np.array(fp)}))
    for i, fp in enumerate(fingerprints2):
        queries.append(Spectrum(mz=np.array([100, 200.]),
                                intensities=np.array([0.7, 0.2]),
                                metadata={"spectrumid": 'query_spec_'+str(i),
                                          "fingerprint": np.array(fp)}))

    # Create Scores object by calculating dice scores
    similarity_measure = FingerprintSimilarity("dice")
    scores = calculate_scores(references, queries, similarity_measure)
    return scores


def test_get_top_hits():
    scores = create_dummy_scores()
    idx_ref, scores_ref = get_top_hits(scores, top_n=10, search_by="references")

    expected_scores_ref = np.array([[0.66666667, 0.5       , 0.        ],
                                    [0.66666667, 0.5       , 0.        ],
                                    [0.66666667, 0.66666667, 0.5       ],
                                    [0.8       , 0.5       , 0.5       ],
                                    [1.        , 0.8       , 0.5       ]])
    expected_idx_ref = np.array([[0, 2, 1],
                                 [1, 2, 0],
                                 [1, 0, 2],
                                 [2, 1, 0],
                                 [0, 2, 1]])
    assert np.allclose(scores_ref, expected_scores_ref, atol=1e-5), \
        "Expected different selected scores"
    assert np.allclose(idx_ref, expected_idx_ref, atol=1e-5), \
        "Expected different selected indices"

    idx_query, scores_query = get_top_hits(scores, top_n=10, search_by="queries")

    expected_scores_query = np.array([[1.        , 0.66666667, 0.66666667, 0.5       , 0.        ],
                                      [0.66666667, 0.66666667, 0.5       , 0.5       , 0.        ],
                                      [0.8       , 0.8       , 0.5       , 0.5       , 0.5       ]])
    expected_idx_query = np.array([[4, 2, 0, 3, 1],
                                 [2, 1, 4, 3, 0],
                                 [4, 3, 2, 1, 0]])
    assert np.allclose(scores_query, expected_scores_query, atol=1e-5), \
        "Expected different selected scores"
    assert np.allclose(idx_query, expected_idx_query, atol=1e-5), \
        "Expected different selected indices"

    # Test lower top_n
    idx_ref, scores_ref = get_top_hits(scores, top_n=2, search_by="references")
    idx_query, scores_query = get_top_hits(scores, top_n=2, search_by="queries")
    assert np.allclose(scores_ref, expected_scores_ref[:,:2], atol=1e-5), \
        "Expected different selected scores"
    assert np.allclose(idx_ref, expected_idx_ref[:,:2], atol=1e-5), \
        "Expected different selected indices"
    assert np.allclose(scores_query, expected_scores_query[:,:2], atol=1e-5), \
        "Expected different selected scores"
    assert np.allclose(idx_query, expected_idx_query[:,:2], atol=1e-5), \
        "Expected different selected indices"

def test_create_network():
    """Test creating a graph from a Scores object"""
    cutoff=0.7
    scores = create_dummy_scores()
    msnet = create_network(scores, cutoff=cutoff)
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
