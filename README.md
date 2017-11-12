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

- Rama,  T.,  J.  Wahle,  P.  Sofroniev,  and  G.  Jager  (2017). [Fast  and  un-supervised  methods  for  multilingual  cognate  clustering](https://arxiv.org/pdf/1702.04938.pdf). *arXiv preprint arXiv:1702.04938*.
- Rama, T., P. Kolachina, and S. Kolachina (2013). [Two methods for automatic identification  of  cognates](http://wwwling.arts.kuleuven.be/QITL5/QITL5-proceedings.pdf#page=84). In *Proceedings of the 5th QITL Conference*,  pp.76–80.
- Kondrak, G. (2003).  [Identifying Complex Sound Correspondences in Bilingual Wordlists](http://webdocs.cs.ualberta.ca/~kondrak/papers/cic03.pdf). In *International Conference on Intelligent Text Processing and Computational Linguistics*, pp. 432–443.
- Kondrak,  G.  (2009).  [Identification  of  Cognates  and  Recurrent  Sound  Correspondences in Word Lists](http://atala.org/IMG/pdf/TAL-2009-50-2-08-Kondrak.pdf). *TAL 50*(2), 201–235. 
- Oakes, M. P. (2000). [Computer Estimation of Vocabulary in a Protolanguage from Word Lists in Four Daughter Languages](http://www.sfs.uni-tuebingen.de/~roland/Literature/Oakes(2000)-computer-estimation-proto-language-cognate-detection.pdf). *Journal of Quantitative Linguistics 7*(3), 233-243.

## Available data, tools, resources

Data:
- [NorthEuraLex](http://northeuralex.org/): a database containing wordlists for many languages spoken in Northern Eurasia. The wordlists consist of translations of >1.000 concepts. The words have been transcribed into IPA.

## Project members

- Verena Blaschke (verenablaschke)
- Maxim Korniyenko (korniyenkoMaxim) 