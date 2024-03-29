# -*- coding: utf-8 -*-
"""fasttext_trainer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nbstFmoApJZVrXtqGSHmlZj_2778saiP

# downloading and installing fastext
"""

# Commented out IPython magic to ensure Python compatibility.
! git clone https://github.com/facebookresearch/fastText.git
# % cd fastText
! mkdir build
# % cd build
! cmake ..
! make && make install
# % cd ..
# % cd ..
! mkdir result
! pip install fasttext
import fasttext

"""#(optional) creaing the input.txt
downloading the raw text of a persian raw text corpus.

**NOTE**: it is recommended that you don't download the whole file which is roughly 70 GB , instead stop the execution after the downloaded volume satisfies your need. by default we'll need about 5 GB so you could stop the excution of the cell after it has downloaded about 6 GB.
"""

!wget https://storage.googleapis.com/danielk-files/farsi-text/merged_files/all_text_merged_cleaned.txt

"""creating the input from the raw text.

size of the input.txt is determined by **input_size** in GB
"""

input_size = 5 # input by GB (~= 570 Million words, 100k unique words)

bytes_to_copy = (input_size) * (10**9) * (0.6)
copied_size = 0
with open('input.txt','a',encoding="UTF-8")as w:
  with open('all_text_merged_cleaned.txt','r',encoding="UTF-8")as r:
    while True:
      chunk = r.read(10000000)
      if not chunk or copied_size >= bytes_to_copy:
        break
      copied_size += 10000000
      w.write(chunk)
      print(f"\r input_size ~= {str((copied_size/1000000)/(0.6))[:6]} MB", end="")
print("\ninput.txt is ready")

"""# training the model
once you have you data in an **input.txt** you can run the below cell
"""

output_name = "/content/result/per_model_"
print(output_name)
! '/content/fastText/build/fasttext' skipgram -input '/content/input.txt' -output $output_name -epoch 5 -minn 3 -maxn 5 -dim 100 -lr 0.1

"""# loading the model
then testing on some random words to check it
"""

model = fasttext.load_model(output_name)

print(model.get_nearest_neighbors('همسر'))
print(model.get_nearest_neighbors('مرد'))
print(model.get_nearest_neighbors('امام'))
print(model.get_nearest_neighbors('تره'))
print(model.get_nearest_neighbors('گلابی'))
print(model.get_nearest_neighbors('سیب'))

print(model.get_analogies("تهران", "ایران", "آلمان"))
print("->برلین")
print(model.get_analogies("تهران", "ایران", "فرانسه"))
print("->پاریس")
print(model.get_analogies("تهران", "ایران", "انگلستان"))
print("->لندن")
print(model.get_analogies("تهران", "ایران", "آمریکا"))
print("->واشنگتن")
print(model.get_analogies("پسر", "مرد", "زن"))
print("->دختر")
print(model.get_analogies("ملکه", "پادشاه", "شوهر"))
print("->زن")
print(model.get_analogies("فرزند", "پدر", "پدربزرگ"))
print("->پدر")

# printing the distance between any two word vectors
x = model.get_word_vector("زن")
y = model.get_word_vector("مرد")
print(np.linalg.norm(x-y))

"""*(also optional)* : the below code downloads the **already trained** persian fastext model. (on wikipidia data, you can check the details here: https://fasttext.cc/docs/en/crawl-vectors.html)

the model would then be in a **wiki.fa.bin** file.

the word vectors would be in a **wiki.fa.vec** file
"""

! wget https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.fa.zip
!unzip wiki.fa.zip
