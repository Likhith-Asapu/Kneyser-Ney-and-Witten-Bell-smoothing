# Kneyser-Ney and Witten Bell smoothing in Python 

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


This repository contains the code for the implementation of Kneyser-Ney and Witten Bell smoothing techniques from scratch in Python.

## Instructions

To run the code make sure the given packages are installed  `re,collections,random and sys`.

The code can be run by entering the following command:

`$ python3 language_model.py <n_value> <smoothing_type> <path_to_corpus> `

**<n_value>** - Value of N-gram or N-gram count(eg. 2 for using bigrams)

**<smoothing_type>** - Enter k to use Kneyser-Ney smoothing and w to use Witten bell smoothing

**<path_to_corpus>** - Replace this with path to the file containing training data.

You are allowed to enter only one sentence at a time.

## Perplexity 

The perplexity scores can be found by running the perp_score.py file.

`$ python3 perp_score.py <n_value> <smoothing type> <path to corpus>  <type>`

**< type >** - values = ("test" / "train") - Refers to whether test data should be used for perplexity calculation or train data

Example - `python3 perp_score.py 4 w medical-corpus.txt test` 

The average perplexity score present at the bottom of the file. The path to corpus will containing both training and testing data.

## Code Testing

The code has been tested on the following corpora:
- EuroParl corpus
- Medical Abstracts corpus

<table>
    <thead>
        <tr>
            <th> </th>
            <th colspan=2>EuroParl corpus</th>
            <th colspan=2>Medical Abstracts corpus</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td> </td>
            <td>Test</td>
            <td>Train</td>
            <td>Test</td>
            <td>Train</td>
        </tr>
        <tr>
            <td>4-gram LM + Kneyser-Ney smoothing</td>
            <td>192.59</td>
            <td>27.63</td>
            <td>407.53</td>
            <td>5.04</td>
        </tr>
        <tr>
            <td>4-gram LM + Witten-Bell smoothing</td>
            <td>54.89</td>
            <td>51.40</td>
            <td>57.00</td>
            <td>3.61</td>
        </tr>
    </tbody>
</table>

- **LM_1**: tokenization + 4-gram LM + Kneyser-Ney smoothing on EuroParl corpus
- **LM_2**: tokenization + 4-gram LM + Witten-Bell smoothing on EuroParl corpus
- **LM_3**: tokenization + 4-gram LM + Kneyser-Ney smoothing on Medical Abstracts corpus
- **LM_4**: tokenization + 4-gram LM + Witten-Bell smoothing on Medical Abstracts corpus


