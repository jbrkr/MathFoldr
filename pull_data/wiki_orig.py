# Go to https://meta.wikimedia.org/wiki/Data_dump_torrents#English_Wikipedia
# Torrent the multistream, English_Wikipedia
## notes from WMF:
#pages-articles.xml.bz2 and pages-articles-multistream.xml.bz2 both contain the same xml contents. So if you unpack either, you get the same data. But with multistream, it is possible to get an article from the archive without unpacking the whole thing. Your reader should handle this for you, if your reader doesn't support it it will work anyway since multistream and non-multistream contain the same xml. The only downside to multistream is that it is marginally larger. You might be tempted to get the smaller non-multistream archive, but it will unpack to ~5-10 times its original size.

#NOTE THAT the multistream dump file contains multiple bz2 'streams' (bz2 header, body, footer) concatenated together into one file, in contrast to the vanilla file which contains one stream. Each separate 'stream' (or really, file) in the multistream dump contains 100 pages, except possibly the last one.

#How to use multistream?
#For multistream, you can get an index file, pages-articles-multistream-index.txt.bz2. The first field of this index is the number of bytes to seek into the compressed archive pages-articles-multistream.xml.bz2, the second is the article ID, the third the article title.

#Cut a small part out of the archive with dd using the byte offset as found in the index. You could then either bzip2 decompress it or use bzip2recover, and search the first file for the article ID.

#See https://docs.python.org/3/library/bz2.html#bz2.BZ2Decompressor


import bz2
