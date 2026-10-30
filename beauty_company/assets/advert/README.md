# Fictional advert artwork

Original SVG illustrations created with AI assistance for this course prototype:
studio lighting/plinth, a cream jar, and a cleanser pump. They are illustrative
packaging for synthetic catalogue products, not photographs or claims about actual
packaging, ingredients, efficacy or quantities. The rendered film labels this.

SVGs are editable sources; checked-in PNG exports are the runtime assets. No image
library, SVG renderer, external asset URL, download or image/video model is needed
to run the app. The app uses the existing configured FFmpeg/font only. Packaging
selection is bounded: a title containing “cleanser” uses the pump, otherwise the
generic jar. This is an illustration choice, not product-evidence validation.

These assets are part of the source ZIP. Do not remove them during deployment.
Missing artwork fails generation explicitly; it does not create a fallback video
or review. Existing saved MP4s/recovery use their saved bytes/hash, not these assets.

PNG exports were made from the paired SVGs with the development machine's existing
Sharp library. Sharp is not an application dependency; any SVG editor/exporter can
produce a replacement PNG after an intentional artwork change. Check the actual
new film and request fresh review; do not replace an already reviewed artifact.

中文：这些是为课程虚构产品原创绘制的包装／影棚示意，非商品实拍，不增加任何功效或规格事实。
SVG 可编辑，已提供运行用 PNG，无须额外图像库／模型。素材随源码包分发，缺失会明确失败。
旧视频与恢复始终使用原文件和哈希，不会因为素材更新而替换已审版本。
