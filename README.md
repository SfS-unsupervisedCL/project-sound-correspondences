# Identifying Sound Correspondence Rules in Bilingual Wordlists

## Motivation

Identifying regular, systematic sound correspondences between the vocabularies of two or more languages is a key method of historical linguistics. Given a large set of such correspondences, it can be surmised that the languages share a common ancestor. 

To establish these correspondences, we can first try to identify potential cognates -- words that share a common origin (cognates often have retained similar meanings, but not always). The next step is to establish regular correspondences between the potential cognates. The underlying sound changes can be conditioned by specific contexts only (ie., specific neighbouring phonemes, position of a phoneme within a word or syllable, etc.). 

Example: (medial/final) /t/ : /s/ in Swedish and German

|              | Swedish | German  |
|--------------|---------|---------|
| (to) eat     | ɛːta    | ɛsən    |
| white        | viːt    | vaɪ̯s    |
| (to) measure | mɛːta   | mɛsən   |
| (to) flow    | flyːta  | fliːsən |
| foot         | fuːt    | fuːs    |

Our research questions are: 
- Can we identify sound correspondence rules between cognate languages in an unsupervised manner?
- How well does this work: How complicated can the rule contexts be? How does such an unsupervised system compare to similar supervised methods or to non-computational methods?

## Method

data:
- see below. We will pick languages from language families that we are familiar with (Germanic, Slavic, Romance).

method:
1. pre-processing: determine which word pairs are potential cognates (using a distance measuring algorithm? (weighted Levenshtein distance?))
2. align the sound segments of the potential cognates
3. compute the similarity scores between aligned sound segments (-> pointwise mutual information)
4. use the information from step 3 to do new alignments
5. repeat 3 & 4 until new iterations do not significantly change the similarity scores anymore

to consider:
- contexts, abstraction
- borrowing, false cognates
- encode phonetic information? (presumably, correspondences between 'similar' sounds are more likely than between very different sounds)

## Relevant literature 

unsupervised cognate identification (incl. identification of sound correspondences) using PMI:
- Rama,  T.,  J.  Wahle,  P.  Sofroniev,  and  G.  Jager  (2017). [Fast  and  unsupervised  methods  for  multilingual  cognate  clustering](https://arxiv.org/pdf/1702.04938.pdf). *arXiv preprint arXiv:1702.04938*.
  - The PMI method in this paper is based on this paper:
    Jäger, G. (2013). [Phylogenetic inference from word lists using weighted alignment with empirically determined weights](http://booksandjournals.brillonline.com/content/journals/10.1163/22105832-13030204). _Language Dynamics and Change, 3_(2), 245-291.
- Rama, T., P. Kolachina, and S. Kolachina (2013). [Two methods for automatic identification  of  cognates](http://wwwling.arts.kuleuven.be/QITL5/QITL5-proceedings.pdf#page=84). In *Proceedings of the 5th QITL Conference*,  pp.76–80.
- Kondrak, G. (2003). [Identifying Complex Sound Correspondences in Bilingual Wordlists](http://webdocs.cs.ualberta.ca/~kondrak/papers/cic03.pdf). In *International Conference on Intelligent Text Processing and Computational Linguistics*, pp. 432–443.

this paper uses multiple characteristics for identifying cognates ("recurrent sound correspondences, phonetic similarity, and semantic affinity") and gives an overview of several existing approaches:
- Kondrak,  G.  (2009).  [Identification  of  Cognates  and  Recurrent  Sound  Correspondences in Word Lists](http://atala.org/IMG/pdf/TAL-2009-50-2-08-Kondrak.pdf). *TAL 50*(2), 201–235.

the following paper uses phonetic information and a Levenshtein-like algorithm for transforming a word into a translation that is a  (potential) cognate:
- Oakes, M. P. (2000). [Computer Estimation of Vocabulary in a Protolanguage from Word Lists in Four Daughter Languages](http://www.sfs.uni-tuebingen.de/~roland/Literature/Oakes(2000)-computer-estimation-proto-language-cognate-detection.pdf). *Journal of Quantitative Linguistics 7*(3), 233-243.

this paper uses a decision tree algorithm and takes into account the phoneme's left and right contexts:
- Hoste, V., Daelemans, W., & Gillis, S. (2004). [Using Rule-Induction Techniques to Model Pronunciation Variation in Dutch](https://www.clips.uantwerpen.be/~gillis/pdf/20040107.9620.cslfinal.pdf). *Computer Speech & Language, 18*(1), 1-23.

TODO have a look at:
- [Learning Bias and Phonological-Rule Induction](https://www.aclweb.org/anthology/J/J96/J96-4003.pdf)
- [Phonetic Alignment and Similarity](https://link.springer.com/content/pdf/10.1023%2FA%3A1025071200644.pdf)
- [Determining Recurrent Sound Correspondences by Inducing Translation Models](http://www.anthology.aclweb.org/C/C02/C02-1016.pdf)
- LexStat: Automatic Detection of Cognates in Multilingual Wordlists: [slides](http://lingulist.de/documents/lexstat.pdf), [paper](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.361.8694&rep=rep1&type=pdf)

## Available data, tools, resources

Data:
- [NorthEuraLex](http://northeuralex.org/): a database containing wordlists for many languages spoken in Northern Eurasia. The wordlists consist of translations of >1.000 concepts. The words have been transcribed into IPA.

Tools:
- [nwalign 0.3.1](https://pypi.python.org/pypi/nwalign/?): Needleman-Wunsch global sequence alignment. As long as it uses cython and numpy it is also a very efficient tool.
- [python-Levenshtein 0.12.0](https://pypi.python.org/pypi/python-Levenshtein/0.12.0): Python extension for computing string edit distances and similarities. Uses Python C.
- [editdistance 0.4](https://pypi.python.org/pypi/editdistance): One more implementation of Levenshtein distance.

## Project members

- Verena Blaschke (verenablaschke)
- Maxim Korniyenko (korniyenkoMaxim) 