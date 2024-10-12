Seorang penjahat dunia maya yang cerdas telah menyembunyikan data rahasia di dalam sebuah file yang terlihat tidak mencurigakan. Dia menggunakan teknik canggih untuk mengubur data ini jauh di dalam beberapa lapisan file. Kamu ditugaskan untuk menemukan data rahasia dan mengungkap flag yang tersembunyi. Hanya penyelidik berpengalaman yang dapat melewati labirin ini.

Tugas kamu adalah menelusuri berbagai lapisan file, menemukan anomali yang mencurigakan, dan akhirnya mengungkap data yang disembunyikan dengan teknik steganografi serta log yang dienkripsi.

 [expert_challenge.zip](https://ssctf.id/files/e44f003d3d6a17a09cccb03bd1ea7118/expert_challenge.zip?token=eyJ1c2VyX2lkIjoyNDEsInRlYW1faWQiOjI2LCJmaWxlX2lkIjoxNH0.ZwnkUQ.w7p5-s05MrKuYsBo2tEPaBN0T2E)

# Solve
```bash
binwalk -e expert_challenge.zip
```