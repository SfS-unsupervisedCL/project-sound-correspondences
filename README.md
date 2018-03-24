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

## How to run the code

We adapted the structure of the imports to allow relative imports from ```preprocessing``` into ```tree```. In order to run the scripts with this import structure, it is necessary to run them as modules from the parent directory (i.e., ```project-sound-correspondences```), e.g.

```
python -m preprocessing.merge_lists deu data\deu.csv swe data\swe.csv data
python -m preprocessing.features data\rus-ukr-all.csv data\ipa_numerical.csv 0.4
python -m tree.tree data\deu-swe-features.csv output
python -m test.ruletest -v
```

## Method

Data:
- see below. We will pick languages from language families that we are familiar with (Germanic, Slavic, Romance).

Preprocessing:
- [x] construct bilingual word lists
- [x] encode IPA symbols as collections of values for phonetic features
  - maybe like this:
  - [x] TSV file where more IPA characters and/or features can easily be added (first column: IPA character, subsequent columns: features)
  - [x] class for sound instances where fields store the values for the features
    - the advantage of doing this instead of using feature dictionaries (eg. manner['b']='plosive') is that we can also use instances of this class during imputation & evalutation.
- [x] eliminate unlikely candidates for cognates
  - [x] write a modified version of the Levenshtein distance that computes the replacement costs based on the sounds' phonetic features
    - ie., if we have _n_ features, then each feature change costs _1/n_
    - we could consider giving different weights to different features
    - [x] for features with values that fall on a scale, we could even consider giving different weights to different changes?
  - [x] write a method that take list_of_pairs and threshold_value as arguments and return the possible cognates
  - [x] determine a good threshold (NED = 0.5?)

The first 10 potential cognates determined by ```utils.get_cognates(file='data/deu-swe-all.csv', threshold=0.5)```:
- ```#``` is the initial word boundary; ```*``` is the empty string (used for insertion/deletion).
- The format is ```(German, Swedish, edit distance)```.

```
(['#', 'a', 'ʊ̯', 'ɡ', 'ə'], ['#', 'øː', '*', 'ɡ', 'a'], 0.29)
(['#', 'oː', '*', 'ɐ̯'], ['#', 'œː', 'r', 'a'], 0.36)
(['#', 'n', 'aː', 'z', 'ə'], ['#', 'n', 'ɛː', 's', 'a'], 0.09)
(['#', 'm', 'ʊ', 'n', 't'], ['#', 'm', 'ɵ', 'n', '*'], 0.24)
(['#', 't͡s', 'aː', 'n', '*'], ['#', 't', 'a', 'nː', 'd'], 0.27)
(['#', 't͡s', 'ʊ', 'ŋ', 'ə'], ['#', 't', 'ɵ', 'ŋː', 'a'], 0.13)
(['#', 'l', 'ɪ', 'p', 'ə'], ['#', 'l', 'ɛ', 'pː', '*'], 0.27)
(['#', 'v', 'a', 'ŋ', 'ə'], ['#', 'ɕ', 'ɪ', 'nː', 'd'], 0.33)
(['#', 'ɡ', 'ə', 'z', '*', 'ɪ', 'ç', 't', '*'], ['#', '*', 'a', 'nː', 's', 'ɪ', 'k', 't', 'ə'], 0.41)
(['#', 'h', 'aː', 'ɐ̯'], ['#', 'h', 'oː', 'r'], 0.31)
```

The same for ```utils.get_cognates(file='data/rus-ukr-all.csv', threshold=0.5)```:
- ```(Russian, Ukrainian, edit distance)```

```
(['#', '*', 'uˑ', 'x', 'ə'], ['#', 'w', 'u', 'x', 'ɔ'], 0.27)
(['#', 'n', 'ɔˑ', 's'], ['#', 'nʲ', 'i', 's'], 0.11)
(['#', 'r', 'ɔˑ', 't'], ['#', 'r', 'ɔ', 't'], 0.03)
(['#', 'z', 'uˑ', 'p'], ['#', 'z', 'u', 'b'], 0.06)
(['#', 'j', 'ɐ', 'z', 'ɨˑ', 'k'], ['#', 'j', 'ɑ', 'z', 'ɪ', 'k'], 0.09)
(['#', 'ɡ', 'u', 'b', 'aˑ'], ['#', 'ɦ', 'u', 'b', 'ɑ'], 0.09)
(['#', 'ʃʲː', '*', 'ɪ', 'k', 'aˑ'], ['#', 'ʂ', 'ʈ͡ʂ', 'ɔ', 'k', 'ɑ'], 0.3)
(['#', 'ɫ', 'ɔˑ', 'p'], ['#', 'l', 'ɔ', 'b'], 0.11)
(['#', 'v', 'ɔˑ', 'ɫ', 'ə', 's', '*'], ['#', 'w', 'ɔ', 'l', 'ɔ', 'sʲː', 'ɑ'], 0.3)
(['#', 'v', 'ɔˑ', 'ɫ', 'ə', 's', 'ɨ'], ['#', 'w', 'ɔ', 'l', 'ɔ', 'sʲː', 'ɑ'], 0.19)
```

Method (feature selection based on Wettig et al. 2012; see also the [slides](https://github.com/SfS-unsupervisedCL/project-sound-correspondences/blob/master/doc/Decision%20Trees%20and%20Wettig%20et%20al%202012.pdf) in [doc](https://github.com/SfS-unsupervisedCL/project-sound-correspondences/blob/master/doc/) folder):
- [x] align word pairs on a symbol level
  - [x] use the phone distances for the alignment (instead of vanilla Needleman-Wunsch)
  - [x] encode empty strings as phones
  - [x] prefix a special word-boundary phone to each word
- [ ] create feature- and level-based decision trees for the aligned symbols (input: source sound, output: target sound) 
  - [x] position features: identify previous vowel/consonant etc. for each symbol
  - [x] for each phone in a word, determine corresponding phones for each position and create feature sets (e.g. _sourceLang\_itself\_voiced=true_, _targetLang\_prevConsonant\_manner=plosive_, etc.)
  - [x] transform the (string) features into features the decision tree packages can work with (integers) (this way, we could also take advantage of the implicit scales that some of the features describe, e.g. vowel height, place of consonant articulation, etc.)
  - [x] write a method generate_instances(levels, positions, features, n_samples) that returns a matrix of size (n_samples x n_features) and a parallel list[str] which contains a list of all the features types
  - [x] for each level (i.e. _source_, _target_) and feature combination (e.g. _target\_manner_), create a set of labelled feature sets
  - [x] build one tree for each level-feature combination (see below in the _Available data, tools, resources section_ for package options)
  - [x] export the trees
  - [ ] export the rules
      - [x] Perform a tree-traversal to get the rules.
      - [x] Merge rules that describe sibling leaf nodes that predict the same class.
      - [ ] Switch back from numerical values to categorical ones.
      - [ ] Combine rules that predict the same classes?
  - Possible improvements:
      - [ ] trim the trees: play around with values for min_samples_split/min_samples_leaf, min_impurity_decrease
        - Unfortunately, it appears that sklearn does not allow us to prevent splits that result in sibling nodes predicting the same category.
      - [x] exclude prevOrSelf_ in certain cases
      - [ ] exclude vowels for cons prediction and other way around

Evaluation:
- [x] imputation and normalized edit distance using the modified  NED/Levenshtein distance from the preprocessing step
- human-readable version: transform imputed sounds into IPA symbols 
  - /!\ some feature combinations are impossible and cannot be represented by IPA symbols
  - use some sort of error symbol to mark impossible feature combinations?
  - alternative: pick closest IPA symbol (within reason?)
- time permitting, we might be able to compute precision values for the generated rules (lit research!)
- doing the literature research necessary for calculating recall/F1-score would be likely be extremely time-consuming

## Notes

- We originally considered working with PMI-based one-to-one alignments of symbols, but switched to the decision-tree-based induction of correspondence rules based on phonetic features and contextual information (similar to Wettig et al. 2012) because we think that this might help us capture more complex correspondences. 
- The encoding of phonetic features in Wettig et al. is somewhat particular to Uralic languages.
  - 2-3 different vowel lengths should be enough (3 because the Russian words include half-long sounds).
  - +/- nasalization feature for vowels (Romance languages)
  - Including stress could be informative, but that information is not included in the NorthEuraLex dataset/
  - We expanded the "secondary features of consonantal articulation" category (palatalization).
  - Time permitting, we could make the features configurable so that it would be possible to add additional features (tone, airstream etc.).
- Our method deviates from Wettig et al.'s method in one significant way: They start with random alignments, and improve the alignments and trees in an expectation-maximization-like algorithm. We start with phonetically motivated assignments, which already yield satisfactory results, and build the trees just once. 
  - We need to include a phonetic distance measure anyway to determine potential cognates within our data sets, since we do not have a cognate-only word list.
- The positional features only capture a symbol's left-hand context. In future projects, including the right-hand context would be interesting.

## Relevant literature 

A decision-tree algorithm using contexts and phonological features:
- Wettig, H., Reshetnikov, K., & Yangarber, R. (2012). [Using context and phonetic features in models of etymological sound change](https://pdfs.semanticscholar.org/d2ea/1dbe1a81f60f99dab04dffc957622b8cb9f2.pdf). _In Proceedings of the EACL 2012 Joint Workshop of LINGVIS & UNCLH_ (pp. 108-116). Association for Computational Linguistics.

A decision tree algorithm taking into account each segment's left and right contexts:
- Hoste, V., Daelemans, W., & Gillis, S. (2004). [Using Rule-Induction Techniques to Model Pronunciation Variation in Dutch](https://www.clips.uantwerpen.be/~gillis/pdf/20040107.9620.cslfinal.pdf). *Computer Speech & Language, 18*(1), 1-23.

Unsupervised cognate identification (incl. identification of sound correspondences) using PMI:
- Rama,  T.,  J.  Wahle,  P.  Sofroniev,  and  G.  Jager  (2017). [Fast  and  unsupervised  methods  for  multilingual  cognate  clustering](https://arxiv.org/pdf/1702.04938.pdf). *arXiv preprint arXiv:1702.04938*.
  - The PMI method in this paper is based on this paper:
    Jäger, G. (2013). [Phylogenetic inference from word lists using weighted alignment with empirically determined weights](http://booksandjournals.brillonline.com/content/journals/10.1163/22105832-13030204). _Language Dynamics and Change, 3_(2), 245-291.
- Rama, T., P. Kolachina, and S. Kolachina (2013). [Two methods for automatic identification  of  cognates](http://wwwling.arts.kuleuven.be/QITL5/QITL5-proceedings.pdf#page=84). In *Proceedings of the 5th QITL Conference*,  pp.76–80.
- Kondrak, G. (2003). [Identifying Complex Sound Correspondences in Bilingual Wordlists](http://webdocs.cs.ualberta.ca/~kondrak/papers/cic03.pdf). In *International Conference on Intelligent Text Processing and Computational Linguistics*, pp. 432–443.

This paper uses multiple characteristics for identifying cognates ("recurrent sound correspondences, phonetic similarity, and semantic affinity") and gives an overview of several existing approaches:
- Kondrak,  G.  (2009).  [Identification  of  Cognates  and  Recurrent  Sound  Correspondences in Word Lists](http://atala.org/IMG/pdf/TAL-2009-50-2-08-Kondrak.pdf). *TAL 50*(2), 201–235.

The following paper uses phonetic information and a Levenshtein-like algorithm for transforming a word into a translation that is a (potential) cognate:
- Oakes, M. P. (2000). [Computer Estimation of Vocabulary in a Protolanguage from Word Lists in Four Daughter Languages](http://www.sfs.uni-tuebingen.de/~roland/Literature/Oakes(2000)-computer-estimation-proto-language-cognate-detection.pdf). *Journal of Quantitative Linguistics 7*(3), 233-243.

more:
- [Learning Bias and Phonological-Rule Induction](https://www.aclweb.org/anthology/J/J96/J96-4003.pdf)
- [Phonetic Alignment and Similarity](https://link.springer.com/content/pdf/10.1023%2FA%3A1025071200644.pdf)
- [Determining Recurrent Sound Correspondences by Inducing Translation Models](http://www.anthology.aclweb.org/C/C02/C02-1016.pdf)
- LexStat: Automatic Detection of Cognates in Multilingual Wordlists: [slides](http://lingulist.de/documents/lexstat.pdf), [paper](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.361.8694&rep=rep1&type=pdf)
- [LingPy](http://lingpy.org/): a Python library for quantitative historical linguistics

## Available data, tools, resources

Data:
- [NorthEuraLex](http://northeuralex.org/): Johannes Dellert and Gerhard Jäger (eds.). 2017. NorthEuraLex (version 0.9).
  - a database containing wordlists for many languages spoken in Northern Eurasia. The wordlists consist of translations of >1.000 concepts. The words have been transcribed into IPA.

Packages for decision tree learning:
- Python:
  - [sklearn's decision tree package](http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)
- R:
  - [rpart](https://cran.r-project.org/web/packages/rpart/rpart.pdf)
  - [party](https://cran.r-project.org/web/packages/party/party.pdf)

## Project members

- Verena Blaschke ([@verenablaschke](https://github.com/verenablaschke))
- Maxim Korniyenko ([@korniyenkoMaxim](https://github.com/korniyenkomaxim)) 
