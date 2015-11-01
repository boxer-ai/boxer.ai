<<<<<<< HEAD
# Banker.ai
we're iterating..

## Installation
TODO: Describe the installation process

## Usage
TODO: Write usage instructions

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History
TODO: Write history

## Credits
@jmontroy90@gmail.com
@avi.yashchin@gmail.com

## License
TODO: Write license
=======
# Semantic fingerprinting with company descriptions

To obtain semantic fingerprints of companies we must use the Cortical API.

One can interact with the API in various ways. You can use the web client or a local client. For the purposes of this paper we used a local client. Cortical have local clients for the Java, PHP, and Python programming languages however due to our familiarity with the Python programming language we’ve chosen to use the Python client. You can download a folder with the files and scripts used in this research paper.

###	Tools

The tools used for this project were:

*	Cortical API (2.2.0)
*	Cortical API key
*	Python 2.7 with Requests extension (Anaconda Python distribution)
*	Cortical Python client (v2.2.0)
*	Statistical analysis software


###	Method and code

The code in this repository will generate a list of keywords, a fingerprint vector, and a fingerprint image generated for a given text.

The python script will only run if you add your cortical API key to the apiKey variable on line 18.

Furthermore on line 26 of GenerateFingerprint.py you can change which company description is analysed from the /Company_Descriptions directory.

The script will generate a semantic fingerprint vector, a keywords list, and an image of the fingerprint (in this order). It will generate these for the text (string) written in the body variable on line 20.

#### Output

Running GenerateFingerprint.py will generate the following output:

	[7, 18, 19, 61, 125, 128, 146, 163, 255, 293, 319, 371, 377, 380, 384, 392, 424, 504, 511, 551, 558, 739, 755, 768, 786, 888, 900, 940, 1020, 1141, 1148, 1194, 1212, 1269, 1317, 1324, 1332, 1402, 1438, 1448, 1515, 1569, 1683, 1768, 1822, 1823, 1831, 1918, 1924, 2035, 2053, 2097, 2111, 2137, 2176, 2397, 2493, 2497, 2516, 2517, 2522, 2525, 2616, 2651, 2719, 2782, 2864, 2891, 3104, 3158, 3225, 3286, 3371, 3372, 3451, 3456, 3565, 3772, 3816, 3836, 3945, 3995, 4216, 4219, 4377, 4378, 4421, 4765, 4796, 4888, 4925, 4956, 5016, 5023, 5030, 5114, 5130, 5134, 5183, 5265, 5268, 5269, 5274, 5365, 5398, 5401, 5472, 5523, 5524, 5525, 5526, 5527, 5540, 5656, 5659, 5660, 5661, 5662, 5663, 5664, 5671, 5731, 5781, 5782, 5785, 5792, 5810, 5820, 6010, 6051, 6052, 6068, 6069, 6171, 6176, 6317, 6578, 6610, 6957, 6981, 7219, 7233, 7338, 7427, 7453, 7494, 7606, 7812, 7864, 7917, 8028, 8136, 8212, 8252, 8284, 8326, 8381, 8385, 8389, 8411, 8465, 8486, 8491, 8509, 8510, 8516, 8625, 8639, 8666, 8677, 8721, 8769, 8770, 8780, 8792, 8805, 8875, 8891, 8894, 8895, 8898, 8899, 8919, 8965, 9006, 9011, 9014, 9022, 9023, 9026, 9027, 9046, 9105, 9136, 9144, 9145, 9152, 9153, 9154, 9179, 9198, 9225, 9272, 9276, 9277, 9281, 9302, 9322, 9350, 9351, 9352, 9354, 9360, 9366, 9399, 9405, 9406, 9407, 9484, 9522, 9523, 9525, 9526, 9529, 9530, 9535, 9540, 9609, 9610, 9615, 9651, 9662, 9663, 9706, 9734, 9735, 9737, 9770, 9779, 9790, 9791, 9837, 9842, 9868, 9909, 9910, 9911, 9912, 9917, 10031, 10039, 10040, 10045, 10090, 10145, 10146, 10166, 10167, 10168, 10170, 10171, 10258, 10266, 10269, 10270, 10283, 10284, 10285, 10292, 10293, 10295, 10296, 10298, 10299, 10317, 10413, 10415, 10416, 10424, 10465, 10484, 10535, 10544, 10545, 10553, 10586, 10649, 10663, 10673, 10674, 10675, 10699, 10755, 10782, 10785, 10808, 10809, 10844, 10935, 10936, 10988, 10989, 10993, 11068, 11073, 11081, 11095, 11112, 11168, 11172, 11175, 11193, 11246, 11296, 11300, 11301, 11414, 11424, 11426, 11427, 11504, 11505, 11518, 11555, 11628, 11681, 11682, 11701, 11702, 11711, 11806, 11836, 11842, 11852, 11879, 11883, 11886, 11900, 12003, 12004, 12165, 12263, 12417, 12523, 12651, 12664, 12774, 12897, 12931, 12961, 13024, 13025, 13026, 13034, 13155, 13156, 13161, 13283, 13289, 13310, 13316, 13319, 13325, 13412, 13418, 13419, 13447, 13540, 13541, 13575, 13590, 13653, 13654, 13661, 13669, 13670, 13699, 13727, 13783, 13784, 14026, 14031, 14047, 14083, 14088, 14108, 14183, 14293, 14333, 14412, 14413, 14505, 14536, 14546, 14625, 14667, 14698, 14727, 14855, 14888, 14970, 14996, 15049, 15082, 15094, 15179, 15181, 15182, 15209, 15210, 15243, 15462, 15491, 15563, 15684, 15696, 15721, 15739, 15755, 15783, 15884, 15885, 15887, 15902, 15906, 15907, 15933, 15943, 15998, 16009, 16016, 16017, 16020, 16077, 16143, 16201, 16250, 16259, 16271, 16280, 16327]

	[u'pratt', u'whitney', u'sales', u'aerospace', u'businesses', u'sikorsky', u'products', u'contracts', u'controls', u’subject']

	UTX fingerprint image saved to /Current/Directory/
>>>>>>> 7b583eee10f6c4edb09bb51cd8f849269c6793d3
