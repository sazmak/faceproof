# Обзор: модели, которые отличают настоящих людей от ИИ

Дата: 13.11.2026. Раздел 1, 2 и 4 основаны на поиске в этот день (ссылки рядом). Раздел 3 записан по памяти и перед защитой его нужно сверить с оригинальными статьями.

## 1. Главный вывод из свежих бенчмарков

Открытые детекторы плохо работают «из коробки» на новых генераторах.

- [arXiv:2602.07814](https://arxiv.org/abs/2602.07814) (февраль 2026): 16 методов (23 варианта), 12 датасетов, 2,6 млн изображений, 291 генератор. По пересказу статьи, на коммерческих генераторах (Flux Dev, Firefly v4, Midjourney v7) большинство детекторов даёт в среднем 18–30% точности. Цифру стоит проверить по самой статье.
- [VendorBench-100](https://www.alphaxiv.org/abs/2607.06254) (июль 2026): 36 систем, из них 24 открытых детектора. Коммерческие API в целом лучше. Высокий ROC AUC не гарантирует хорошую работу при фиксированном пороге.
- [AI-GenBench](https://arxiv.org/pdf/2504.20865v3) (2025): генераторы идут по времени выхода, проверяется обобщение на более новые.
- [AIGIBench](https://alphaxiv.org/overview/2505.12335v2) (2025): устойчивость и обобщение, в том числе на картинках из соцсетей.
- [NTIRE 2026](https://www.alphaxiv.org/abs/2604.11487.md): 42 генератора и 36 преобразований изображений, упор на постобработку.

Это и есть мотивация проекта: модель менять не обязательно, сначала нужно дать ей данные нового генератора.

## 2. Помогает ли небольшой набор новых фейков

Да, это подтверждено несколькими работами.

- Li, Sun, Poskitt, [How Generalizable are Deepfake Detectors?](https://ar5iv.labs.arxiv.org/html/2308.04177): в zero-shot детекторы не обобщаются, в few-shot ситуация частично исправляется.
- [ICPR 2024, CLIP + LoRA](https://iris.unimore.it/bitstream/11380/1343567/2/2024_ICPR_Deepfakes.pdf): дообучение всего на 50 парах «настоящее/фейк» обходит сравниваемые бейзлайны на невиданных генераторах.
- [AdaptPrompt](https://arxiv.org/html/2512.17730v1) (препринт): few-shot на 320 изображениях, проверка на 25 тестовых наборах.
- [Korshunov, Marcel, 2021](https://publications.idiap.ch/downloads/papers/2021/Korshunov_TBIOM_2021.pdf): few-shot настройка улучшает детекцию между базами (про видео-дипфейки).
- [FTNet, AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/39998): few-shot без переобучения.

Наши 314 фото попадают в тот же масштаб (50–320 изображений), что и в этих работах.

## 3. Основные научные подходы (по памяти, сверить)

| Метод | Год, площадка | Идея |
|---|---|---|
| CNNDetection (Wang et al.) | CVPR 2020 | ResNet-50, обучен на ProGAN с аугментациями. Хорош на GAN, слаб на диффузии. |
| UnivFD (Ojha et al.) | CVPR 2023 | Замороженный CLIP + линейный слой. Обобщается лучше обученных с нуля. **Наш метод.** |
| DIRE (Wang et al.) | ICCV 2023 | Ошибка реконструкции диффузионной моделью. |
| NPR (Tan et al.) | CVPR 2024 | Следы апсемплинга в соседних пикселях. |
| DRCT (Chen et al.) | ICML 2024 | Контрастное обучение на реконструкциях. |
| AIDE (Yan et al.) | ICLR 2025 | Смысловые признаки CLIP плюс низкоуровневые патчи. |
| Community Forensics (Park, Owens) | CVPR 2025 | Датасет из тысяч генераторов: важнее всего разнообразие генераторов. |
| SPAI (Karageorgiou et al.) | CVPR 2025 | Спектральные признаки. |
| Effort (Yan et al.) | ICML 2025 | Ортогональное разложение весов CLIP. |
| DeepfakeBench (Yan et al.) | NeurIPS 2023 | Единый бенчмарк подделок лиц. |

## 4. Готовые модели на Hugging Face

Точность указана авторами на их собственных тестах, между собой цифры сравнивать нельзя.

| Модель | Основа | Что заявлено |
|---|---|---|
| [SadraCoding/SDXL-Deepfake-Detector](https://huggingface.co/SadraCoding/SDXL-Deepfake-Detector/blob/main/README.md) | ViT, лица | accuracy 86%, ссылается на 140k Real and Fake Faces |
| [desireemcv/vit-face-real-vs-fake](https://huggingface.co/desireemcv/vit-face-real-vs-fake) | ViT-base | accuracy 0,9467, автор предупреждает о слабом обобщении на новые техники |
| [prithivMLmods/Deep-Fake-Detector-v2-Model](https://huggingface.co/prithivMLmods/Deep-Fake-Detector-v2-Model/tree/main) | ViT | метрики не проверены |
| [prithivMLmods/deepfake-detector-model-v1](https://huggingface.co/prithivMLmods/deepfake-detector-model-v1/tree/main) | SigLIP2 | метрики не проверены |
| [Ateeqq/ai-vs-human-image-detector](https://ateeqq-ai-image-detector.hf.space) | SigLIP | метрики не проверены |

### Детекторы, которые запускаются в браузере (ONNX, transformers.js)

Проверено 13.11.2026 через API Hugging Face: смотрели список файлов, `config.json` и карточки моделей.

| Модель | Что это | Решение |
|---|---|---|
| [onnx-community/Deep-Fake-Detector-v2-Model-ONNX](https://huggingface.co/onnx-community/Deep-Fake-Detector-v2-Model-ONNX) | ViT-base 224, классы `Realism` и `Deepfake`, квантованная версия 83 МБ | **Взят как «детектор до улучшения».** Понятные классы, стандартная предобработка. |
| [onnx-community/CommunityForensics-DeepfakeDet-ViT-ONNX](https://huggingface.co/onnx-community/CommunityForensics-DeepfakeDet-ViT-ONNX) | ViT-small 384 из статьи Community Forensics. По карточке: 2,7 млн изображений, 4803 генератора | Не взят: один выход без подписей классов и своя предобработка 440→384. Без проверки на Python есть риск неверно прочитать ответ модели. |
| [onnx-community/deepfake_vs_real_image_detection-ONNX](https://huggingface.co/onnx-community/deepfake_vs_real_image_detection-ONNX) | ViT-base 224, классы `Real` и `Fake` | Запасной вариант. |

## 5. Датасеты

- [140k Real and Fake Faces](https://huggingface.co/datasets/TheKernel01/140k-Real-and-Fake-Faces): 70 тыс. настоящих лиц из FFHQ и 70 тыс. лиц StyleGAN, 256×256. Оригинал на Kaggle: `xhlulu/140k-real-and-fake-faces`. Из него взяты 420 настоящих лиц (первые 420 строк с меткой `real` из части `train`).
- [FFHQ](https://github.com/NVlabs/ffhq-dataset): настоящие лица, лицензия CC BY-NC-SA 4.0 (некоммерческое использование).

## 6. Почему выбран CLIP + линейная голова

1. Это опубликованный метод (UnivFD), а не самодельная архитектура.
2. Обучается за секунды на процессоре: на ноутбуке нет видеокарты и 8 ГБ памяти.
3. Работает в браузере, поэтому интерфейс и эксперимент лежат в одном файле.
4. Между версиями меняются только данные, как требует вариант B.
