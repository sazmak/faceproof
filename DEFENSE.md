# FaceProof — defense pack (English)

Формат по заданию: минимум 7 минут выступления, потом 2–3 минуты вопросов. В тексте около 730 слов: это 6 минут спокойной речи плюс около минуты на демо. Говорите медленно и не сокращайте демо, иначе выйдет меньше 7 минут. Курсивом по-русски написано, что показывать на экране; английский текст можно читать как есть.

Site: https://sazmak.github.io/faceproof/ · Code: https://github.com/sazmak/faceproof

## One sentence to remember

Ready-made detectors guess like a coin on my new AI faces, the same kind of model trained on my new dataset reaches 98.7%, and my own hand test then showed where it still fails.

## Script (about 7 minutes)

### 1. Problem — 1 min
*Показывать: заголовок сайта.*

Hello, my name is ___. My project is called FaceProof. It is an individual project in Computer Vision, option B.

The problem is simple. Detectors that tell a real face from an AI face are trained on old generators. When a new generator appears, they stop working. A benchmark from February 2026 tested sixteen detection methods on images from 291 generators, and its summary reports only 18 to 30 percent accuracy on new commercial generators.

My question was: can I fix this with data, without changing the model?

### 2. Idea and data — 1 min
*Показывать: блок «How it works», карточка 02.*

I generated 420 portraits of people who do not exist, using Google Flow. This is my new dataset. For real faces I took 420 photos from FFHQ, an open dataset of real people.

Then I compared three detectors on the same test images. Two of them never saw my data. The third one was trained on it.

### 3. Preprocessing — 1 min
*Показывать: блок «What the detectors see» с примерами лиц.*

There was a trap here. My images are 1024 by 1024 and show a person to the waist. The real photos are small and cropped to the face. A model could simply learn the framing, not the difference between real and AI.

So every image goes through the same steps: find the face, crop a square around it, resize to 256 by 256, save with the same JPEG quality. 69 of my images were removed because the face was too small. That left 351 generated and 420 real faces.

I found two mistakes in this step by looking at the crops with my own eyes. First, in full-body photos the face was not found at all. Second, the detector sometimes picked a bag or the background instead of a face. I fixed both before the experiment, and the journal in the repository records it.

I split the data once, before any training: 80 percent for training, 20 percent for the test. For my generated images the split keeps every prompt category in both parts.

### 4. Method — 1 min
*Показывать: блок «How it works», абзац под заголовком.*

I used a published method called UnivFD, from CVPR 2023. It has two parts. First, a frozen CLIP model turns each image into 512 numbers. Second, a small logistic regression is trained on these numbers.

CLIP is never changed. Only the data for the small classifier changes. That is why this is option B.

Everything runs in the browser, because my laptop has no GPU and no Python.

### 5. Results — 1.5 min
*Показывать: таблицу, потом график.*

Here are the results on 159 test images: 73 generated and 86 real.

The table has three rows, one per detector, and for each one it shows accuracy, how many AI faces were caught, and how many real faces stayed real.

The open-source detector from Hugging Face: 54.7 percent. It called half of the real people AI. CLIP with no training, where I only ask it in words "real photo or AI-generated": 57.2 percent. It missed more than half of the AI faces. Both are close to a coin flip.

My detector, trained on the new dataset: 98.7 percent. It caught 72 of 73 AI faces and kept 85 of 86 real faces.

The chart shows how many new images are needed. With only 5 generated images accuracy is already 87 percent. With 10 it is 96. With all 278 it is 98.7.

I also ran five-fold cross-validation on all 771 images and got the same 98.7 percent.

### 6. Demo — 1 min
*Показывать: Try the detector, загрузить два файла. Потом включить Live camera.*

Let me show it. This is one of my generated portraits. The detector says: AI-generated.

This is a real photo from FFHQ. The detector says: real photo.

There is also a live camera mode. It checks the face five or six times per second. And this is where I want to be honest about the limits.

### 7. Limitations — 1 min
*Показывать: блок «Limits», первый пункт с жирным началом.*

After training I tested the detector by hand, with other images. On AI faces from other generators and on the webcam it almost always says "real". And it says "AI" more often for dark-skinned faces.

I measured why. The AI score follows warm sunny light, with correlation 0.71, and smiling, with correlation 0.63. My generated portraits are sunny and smiling; the real photos are not. Also, dark-skinned faces are about 19 percent of my generated set but only 5 percent of the real set.

So the detector learned how one generator differs from old amateur photos. It did not learn what AI looks like in general. 98.7 percent is accuracy on my generator, not on every AI image.

The fix is more data: real photos in the same style, and faces from other generators. Thank you. I am ready for questions.

## Demo — что подготовить

1. За 10 минут до выступления открыть сайт и один раз загрузить любое фото в **Try the detector**. При первом запуске скачиваются модели (около 180 МБ), потом они в кэше браузера.
2. Положить на рабочий стол два файла из папки проекта:
   - generated: `data\fake\human_photo_551b11bb.jpg`
   - real: `data\real\ffhq_train_00738.jpg`
3. Проверить оба файла заранее. Загрузку файла на сайте я не тестировал. Через тестовый видеопоток `black_human_photo_f5ce7ade.jpg` получил 98% AI, а `ffhq_train_00738.jpg` 99% real.
4. Камеру показывать как пример ограничения. На живом лице ответ непредсказуем, и это часть рассказа.
5. Если сайт не открывается: в папке проекта выполнить `powershell -ExecutionPolicy Bypass -File serve.ps1` и открыть http://localhost:8765.

## Questions and answers

**Why is this option B and not option A?**
The model is the same in all cases: CLIP plus a linear classifier. What I changed is the data. I built a new dataset and compared detectors that never saw it with a detector trained on it. I also show how accuracy grows with dataset size.

**Which generator did you use?**
Google Flow. All 420 portraits come from it, in eight prompt categories.

**Is 98.7 percent too good to be true?**
Partly, yes, and I checked it. 96 percent with only 10 images means the classes are very easy to separate. The reason is photo style: my portraits are sunny and smiling, FFHQ photos are not. So I call this accuracy on my generator, not a general AI detector.

**Why is the ready-made detector so bad? Did you run it correctly?**
It was trained on other fakes and never saw my generator. Its classes are clearly labelled, "Realism" and "Deepfake", and I used its standard preprocessing. One note: I ran the quantized ONNX version, which can be slightly weaker than the original.

**Why CLIP and not your own neural network?**
With about 600 images, training a network from scratch makes no sense. CLIP already knows how to describe images. This is a published method, UnivFD, and it trains in seconds on a CPU.

**Real photos are 256 pixels, yours are 1024. Is that a hint for the model?**
It would be, so I bring all images to the same form: face crop, 256 by 256, same JPEG quality. This reduces the difference but does not remove it fully. It is listed in the limitations.

**Is there data leakage between training and test?**
No. The split is fixed in a file, `splits/split.json`, with zero overlap. The text prompts for CLIP and the 0.5 threshold were chosen before testing. But the test AI faces come from the same generator as the training ones.

**Is your detector biased against dark-skinned people?**
On outside images, yes, I saw this in my hand test. In my data, dark-skinned faces are about 19 percent of the generated set and 5 percent of the real set, so the model could use this as a signal. Inside my own data it did not change the answers: in cross-validation none of the 21 real dark-skinned faces was called AI. The group shares are estimated with CLIP, so they are approximate.

**Why did you not fix it?**
A fix needs a new real dataset and a new experiment, and I did not have time. I decided it is better to measure the problem and show it than to present 98.7 percent as a general result.

**The test set is small. How reliable is the number?**
159 test images. The 95 percent interval for 98.7 is about 95.5 to 99.7 percent. Cross-validation on 771 images gave the same value.

**What do accuracy, recall and AUC mean?**
Accuracy is the share of correct answers. Recall is the share of AI faces that were caught. AUC shows how well the scores separate the two classes at any threshold: 0.5 is random, 1 is perfect.

**How does the live camera work?**
Each frame goes through the same steps as a photo: find the face, crop, CLIP, classifier. It runs five to six checks per second. The video is not recorded and does not leave the browser.

**Where is the synthetic data?**
The 420 portraits were generated by AI for this project. They are the new part of the dataset.

**What would you do next?**
Real photos in the same style and with the same mix of people. Faces from two or three other generators. A test on a generator that was not in training. And training with camera-like noise for the live mode.

## If they ask to see the code

- `index.html`, function `trainLogReg` — logistic regression, 1200 steps of gradient descent.
- `index.html`, function `faceCrop` — the same preprocessing for every image.
- `splits/split.json` — the fixed train/test split.
- `results/results.json` — metrics and classifier weights.
- `JOURNAL.md` — step-by-step log with times, including the mistakes I found (in Russian).

## Произношение и короткие формы

- UnivFD: «юни-ви-эф-ди». CLIP: «клип». FFHQ: «эф-эф-эйч-кью».
- 98.7%: "ninety-eight point seven percent". 0.71: "zero point seven one".
- logistic regression: «лоджи́стик регре́шн». correlation: «корэле́йшн».

## Checklist

- [ ] Сайт открыт, модели в кэше (заранее загрузить одно фото).
- [ ] Два файла для демо на рабочем столе, оба проверены.
- [ ] Камера разрешена для сайта в браузере.
- [ ] Вкладка с репозиторием на GitHub открыта.
- [ ] Вставить своё имя в первую фразу.
