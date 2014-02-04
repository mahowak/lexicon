##all celex with combinations of 3 lengths for nphone, syll, pcfg and with/without homophones
python celex.py --lemma lemma --language english --mono 1 --homocel 1 --minlength 2 --maxlength 8
python celex.py --lemma lemma --language english --mono 1 --homocel 0 --minlength 2 --maxlength 8 
python celex.py --lemma lemma --language english --mono 1 --homocel 1 --minlength 3 --maxlength 8 
python celex.py --lemma lemma --language english --mono 1 --homocel 0 --minlength 3 --maxlength 8 
python celex.py --lemma lemma --language english --mono 1 --homocel 1 --minlength 4 --maxlength 8 
python celex.py --lemma lemma --language english --mono 1 --homocel 0 --minlength 4 --maxlength 8 
python celex.py --lemma lemma --language english --mono 1 --homocel 1 --minlength 2 --maxlength 8 --syll 1
python celex.py --lemma lemma --language english --mono 1 --homocel 0 --minlength 2 --maxlength 8 --syll 1
python celex.py --lemma lemma --language english --mono 1 --homocel 1 --minlength 3 --maxlength 8 --syll 1
python celex.py --lemma lemma --language english --mono 1 --homocel 0 --minlength 3 --maxlength 8 --syll 1
python celex.py --lemma lemma --language english --mono 1 --homocel 1 --minlength 4 --maxlength 8 --syll 1
python celex.py --lemma lemma --language english --mono 1 --homocel 0 --minlength 4 --maxlength 8 --syll 1
python celex.py --lemma lemma --language english --mono 1 --homocel 1 --minlength 2 --maxlength 8 --pcfg 1
python celex.py --lemma lemma --language english --mono 1 --homocel 0 --minlength 2 --maxlength 8 --pcfg 1
python celex.py --lemma lemma --language english --mono 1 --homocel 1 --minlength 3 --maxlength 8 --pcfg 1
python celex.py --lemma lemma --language english --mono 1 --homocel 0 --minlength 3 --maxlength 8 --pcfg 1
python celex.py --lemma lemma --language english --mono 1 --homocel 1 --minlength 4 --maxlength 8 --pcfg 1
python celex.py --lemma lemma --language english --mono 1 --homocel 0 --minlength 4 --maxlength 8 --pcfg 1

#all models, 2-8 letters, no homophones, no cv
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_2_8.txt --n 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_2_8.txt --n 2
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_2_8.txt --n 3
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_2_8.txt --n 4
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_2_8.txt --n 5
python main.py --homo 0 --model nsyll --iter 30 --corpus celexes/syll__lemma_english_1_1_2_8.txt --n 1
python main.py --homo 0 --model nsyll --iter 30 --corpus celexes/syll__lemma_english_1_1_2_8.txt --n 2
python main.py --homo 0 --model pcfg --iter 30 --corpus celexes/pcfg__lemma_english_1_1_2_8.txt

#all models, 3-8 letters, no homophones, no cv
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_3_8.txt --n 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_3_8.txt --n 2
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_3_8.txt --n 3
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_3_8.txt --n 4
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_3_8.txt --n 5
python main.py --homo 0 --model nsyll --iter 30 --corpus celexes/syll__lemma_english_1_1_3_8.txt --n 1
python main.py --homo 0 --model nsyll --iter 30 --corpus celexes/syll__lemma_english_1_1_3_8.txt --n 2
python main.py --homo 0 --model pcfg --iter 30 --corpus celexes/pcfg__lemma_english_1_1_3_8.txt

#all models, 4-8 letters, no homophones, no cv
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_4_8.txt --n 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_4_8.txt --n 2
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_4_8.txt --n 3
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_4_8.txt --n 4
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_4_8.txt --n 5
python main.py --homo 0 --model nsyll --iter 30 --corpus celexes/syll__lemma_english_1_1_4_8.txt --n 1
python main.py --homo 0 --model nsyll --iter 30 --corpus celexes/syll__lemma_english_1_1_4_8.txt --n 2
python main.py --homo 0 --model pcfg --iter 30 --corpus celexes/pcfg__lemma_english_1_1_4_8.txt


#all models, 2-8 letters, no homophones, no cv
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_2_8.txt --n 1 --cv 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_2_8.txt --n 2 --cv 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_2_8.txt --n 3 --cv 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_2_8.txt --n 4 --cv 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_2_8.txt --n 5 --cv 1
python main.py --homo 0 --model nsyll --iter 30 --corpus celexes/syll__lemma_english_1_1_2_8.txt --n 1 --cv 1
python main.py --homo 0 --model nsyll --iter 30 --corpus celexes/syll__lemma_english_1_1_2_8.txt --n 2 --cv 1
python main.py --homo 0 --model pcfg --iter 30 --corpus celexes/pcfg__lemma_english_1_1_2_8.txt --cv 1

#all models, 3-8 letters, no homophones, no cv
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_3_8.txt --n 1 --cv 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_3_8.txt --n 2 --cv 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_3_8.txt --n 3 --cv 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_3_8.txt --n 4 --cv 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_3_8.txt --n 5 --cv 1
python main.py --homo 0 --model nsyll --iter 30 --corpus celexes/syll__lemma_english_1_1_3_8.txt --n 1 --cv 1
python main.py --homo 0 --model nsyll --iter 30 --corpus celexes/syll__lemma_english_1_1_3_8.txt --n 2 --cv 1
python main.py --homo 0 --model pcfg --iter 30 --corpus celexes/pcfg__lemma_english_1_1_3_8.txt --cv 1

#all models, 4-8 letters, no homophones, no cv
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_4_8.txt --n 1 --cv 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_4_8.txt --n 2 --cv 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_4_8.txt --n 3 --cv 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_4_8.txt --n 4 --cv 1
python main.py --homo 0 --model nphone --iter 30 --corpus celexes/lemma_english_1_1_4_8.txt --n 5 --cv 1
python main.py --homo 0 --model nsyll --iter 30 --corpus celexes/syll__lemma_english_1_1_4_8.txt --n 1 --cv 1
python main.py --homo 0 --model nsyll --iter 30 --corpus celexes/syll__lemma_english_1_1_4_8.txt --n 2 --cv 1
python main.py --homo 0 --model pcfg --iter 30 --corpus celexes/pcfg__lemma_english_1_1_4_8.txt --cv 1

