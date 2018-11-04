#http://www.david-greve.de/luach-code/jewish-python.html

#Example of use:
# import torah
# import sys
# 
# if len(sys.argv) == 5:
#   day = int(sys.argv[1])
#   month = int(sys.argv[2])
#   year = int(sys.argv[3])
#   if sys.argv[4] == "y":
#     diaspora = True
#   else:
#     diaspora = False
#   str = torah.getTorahSections(month, day, year, diaspora)
#   if str != "":
#     print "Torah section(s): " + str
#   else:
#     print "No torah section(s) on that day"
# else:
#   print "Syntax: python sample.py <Day> <Month> <Year> <Diaspora flag: y = Diaspora, n = Israel>"

from common.date_utils import calendar_util

ID_BERESHITH                   = 0
ID_NOAH                        = 1
ID_LEHLEHA                     = 2
ID_VAYERA                      = 3
ID_HAYESARAH                   = 4
ID_TOLEDOTH                    = 5
ID_VAYETSE                     = 6
ID_VAYISHLAH                   = 7
ID_VAYESHEB                    = 8
ID_MIKKETS                     = 9
ID_VAYIGGASH                  = 10
ID_VAYHEE                     = 11
ID_SHEMOTH                    = 12
ID_VAERA                      = 13
ID_BO                         = 14
ID_BESHALLAH                  = 15
ID_YITHRO                     = 16
ID_MISHPATIM                  = 17
ID_TERUMAH                    = 18
ID_TETSAVVEH                  = 19
ID_KITISSA                    = 20
ID_VAYAKHEL                   = 21
ID_PEKUDE                     = 22
ID_VAYIKRA                    = 23
ID_TSAV                       = 24
ID_SHEMINI                    = 25
ID_TAZRIANG                   = 26
ID_METSORANG                  = 27
ID_AHAREMOTH                  = 28
ID_KEDOSHIM                   = 29
ID_EMOR                       = 30
ID_BEHAR                      = 31
ID_BEHUKKOTHAI                = 32
ID_BEMIDBAR                   = 33
ID_NASO                       = 34
ID_BEHAALOTEHA                = 35
ID_SHELAHLEHA                 = 36
ID_KORAH                      = 37
ID_HUKATH                     = 38
ID_BALAK                      = 39
ID_PINHAS                     = 40
ID_MATOTH                     = 41
ID_MASEH                      = 42
ID_DEBARIM                    = 43
ID_VAETHANAN                  = 44
ID_EKEB                       = 45
ID_REEH                       = 46
ID_SHOFETIM                   = 47
ID_KITETSE                    = 48
ID_KITABO                     = 49
ID_NITSABIM                   = 50
ID_VAYELEH                    = 51
ID_HAAZINU                    = 52

ID_SIMHATHTORAH               = 53
ID_SIMHATHTORAH_2             = 54
ID_SIMHATHTORAH_3             = 55

ID_ROSH_HODESH_SHABBAT        = 60
ID_SHEKALIM                   = 61
ID_ZAHOR                      = 62
ID_PARAH                      = 63
ID_HAHODESH                   = 64
ID_HAGGADOL                   = 65
ID_SHUVA                      = 66

ID_ROSH_HASHANAH_I            = 70
ID_ROSH_HASHANAH_II           = 71
ID_FAST_OF_GEDALIAH           = 72
ID_YOM_KIPPUR                 = 73
ID_SUCCOTH_I                  = 74
ID_SUCCOTH_II                 = 75
ID_SUCCOTH_III_NO_SHABBAT     = 76
ID_SUCCOTH_III                = 77
ID_SUCCOTH_IV                 = 78
ID_SUCCOTH_V_NO_SHABBAT       = 79
ID_SUCCOTH_V                  = 80
ID_SUCCOTH_VI_NO_SHABBAT      = 81
ID_SUCCOTH_VI                 = 82
ID_HOSHANAH_RABBAH            = 83
ID_HOL_HAMOED_SUCCOTH         = 84
ID_SHEMINI_AZERETH_1          = 85
ID_FAST_OF_ESTHER             = 86
ID_PURIM                      = 87
ID_FAST_OF_TEVET_10           = 88
ID_PESAH_I                    = 89
ID_HOL_HAMOED_PESAH           = 90
ID_PESAH_VII                  = 91
ID_PESAH_VIII                 = 92
ID_PESAH_VIII_NO_SHABBAT      = 93
ID_SHAVUOTH_I                 = 94
ID_SHAVUOTH_II_NO_SHABBAT     = 95
ID_SHAVUOTH_II                = 96
ID_YOM_HAATZMAUT              = 97
ID_FAST_OF_TAMMUZ_17          = 98
ID_FAST_OF_TISHA_BAV          = 99
ID_CHANUKKAH_I               = 100
ID_CHANUKKAH_II              = 101
ID_CHANUKKAH_III             = 102
ID_CHANUKKAH_IV              = 103
ID_CHANUKKAH_V               = 104
ID_CHANUKKAH_VI              = 105
ID_CHANUKKAH_VI_ROSH_HODESH  = 106
ID_CHANUKKAH_VII             = 107
ID_CHANUKKAH_VII_ROSH_HODESH = 108
ID_CHANUKKAH_VIII            = 109
ID_SECOND_SHABBAT_CHANUKKAH  = 110
ID_ROSH_HODESH               = 111
ID_PESAH_II                  = 112
ID_PESAH_III                 = 113
ID_PESAH_IV                  = 114
ID_PESAH_IV_NOT_SUNDAY       = 115
ID_PESAH_IV_SUNDAY           = 116
ID_PESAH_V                   = 117
ID_PESAH_V_NOT_MONDAY        = 118
ID_PESAH_V_MONDAY            = 119
ID_PESAH_VI                  = 120

ID_SPECIAL_1                  = 150
ID_SPECIAL_2                  = 151
ID_SPECIAL_3                  = 152
ID_SPECIAL_4                  = 153
ID_SPECIAL_5                  = 154
ID_SPECIAL_6                  = 155
ID_SPECIAL_7                  = 156
ID_SPECIAL_8                  = 157
ID_SPECIAL_8A                 = 158
ID_SPECIAL_9                  = 159
ID_SPECIAL_10                 = 161
ID_SPECIAL_11                 = 162
ID_SPECIAL_12                 = 163

ID_SHEMINI_AZERETH_2          = 170
ID_SHEMINI_AZERETH_3          = 171
ID_SHEMINI_AZERETH            = 172

ID_MAX                        = 256

ID_NULL                       = 1000

torahSectionsA = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_SHEKALIM,ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_ZAHOR,   ID_NULL,      # 20
   ID_KITISSA,             ID_PARAH,   ID_NULL,      # 21
   ID_VAYAKHEL,            ID_PEKUDE,  ID_HAHODESH,  # 22
   ID_VAYIKRA,             ID_NULL,    ID_NULL,      # 24
   ID_TSAV,                ID_HAGGADOL,ID_NULL,      # 25
   ID_HOL_HAMOED_PESAH,    ID_NULL,    ID_NULL,      # 26
   ID_SHEMINI,             ID_NULL,    ID_NULL,      # 27
   ID_TAZRIANG,           ID_METSORANG,ID_NULL,      # 28
   ID_AHAREMOTH,           ID_KEDOSHIM,ID_NULL,      # 29
   ID_EMOR,                ID_NULL,    ID_NULL,      # 30
   ID_BEHAR,            ID_BEHUKKOTHAI,ID_NULL,      # 31
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 32
   ID_NASO,                ID_NULL,    ID_NULL,      # 33
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 34
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 35
   ID_KORAH,               ID_NULL,    ID_NULL,      # 36
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 37
   ID_BALAK,               ID_NULL,    ID_NULL,      # 38
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 39
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 40
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 41
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 42
   ID_EKEB,                ID_NULL,    ID_NULL,      # 43
   ID_REEH,                ID_NULL,    ID_NULL,      # 44
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 45
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 46
   ID_KITABO,              ID_NULL,    ID_NULL,      # 47
   ID_NITSABIM,            ID_VAYELEH, ID_NULL,      # 48
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 49
   ID_YOM_KIPPUR,          ID_NULL,    ID_NULL,      # 50
   ID_HOL_HAMOED_SUCCOTH,  ID_NULL,    ID_NULL       # 51
  ]

torahSectionsB = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_SHEKALIM,ID_NULL,      # 18
   ID_TERUMAH,             ID_ZAHOR,   ID_NULL,      # 19
   ID_TETSAVVEH,           ID_NULL,    ID_NULL,      # 20
   ID_KITISSA,             ID_PARAH,   ID_NULL,      # 21
   ID_VAYAKHEL,            ID_PEKUDE,  ID_HAHODESH,  # 22
   ID_VAYIKRA,             ID_NULL,    ID_NULL,      # 23
   ID_TSAV,                ID_HAGGADOL,ID_NULL,      # 24
   ID_PESAH_VII,           ID_NULL,    ID_NULL,      # 25
   ID_SHEMINI,             ID_NULL,    ID_NULL,      # 26
   ID_TAZRIANG,           ID_METSORANG,ID_NULL,      # 27
   ID_AHAREMOTH,           ID_KEDOSHIM,ID_NULL,      # 28
   ID_EMOR,                ID_NULL,    ID_NULL,      # 29
   ID_BEHAR,            ID_BEHUKKOTHAI,ID_NULL,      # 30
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 31
   ID_NASO,                ID_NULL,    ID_NULL,      # 32
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 33
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 34
   ID_KORAH,               ID_NULL,    ID_NULL,      # 35
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 36
   ID_BALAK,               ID_NULL,    ID_NULL,      # 37
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 38
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 39
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 40
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 41
   ID_EKEB,                ID_NULL,    ID_NULL,      # 42
   ID_REEH,                ID_NULL,    ID_NULL,      # 43
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 44
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 45
   ID_KITABO,              ID_NULL,    ID_NULL,      # 46
   ID_NITSABIM,            ID_NULL,    ID_NULL,      # 47
   ID_VAYELEH,             ID_NULL,    ID_NULL,      # 48
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 49
   ID_HOL_HAMOED_SUCCOTH,  ID_NULL,    ID_NULL       # 50
   ]

torahSectionsCDiaspora = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_SHEKALIM,ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_ZAHOR,   ID_NULL,      # 20
   ID_KITISSA,             ID_PARAH,   ID_NULL,      # 21
   ID_VAYAKHEL,            ID_PEKUDE,  ID_HAHODESH,  # 22
   ID_VAYIKRA,             ID_NULL,    ID_NULL,      # 24
   ID_TSAV,                ID_HAGGADOL,ID_NULL,      # 25
   ID_HOL_HAMOED_PESAH,    ID_NULL,    ID_NULL,      # 26
   ID_SHEMINI,             ID_NULL,    ID_NULL,      # 27
   ID_TAZRIANG,           ID_METSORANG,ID_NULL,      # 28
   ID_AHAREMOTH,           ID_KEDOSHIM,ID_NULL,      # 29
   ID_EMOR,                ID_NULL,    ID_NULL,      # 30
   ID_BEHAR,            ID_BEHUKKOTHAI,ID_NULL,      # 31
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 32
   ID_SHAVUOTH_II,         ID_NULL,    ID_NULL,      # 33
   ID_NASO,                ID_NULL,    ID_NULL,      # 34
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 35
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 36
   ID_KORAH,               ID_NULL,    ID_NULL,      # 37
   ID_HUKATH,              ID_BALAK,   ID_NULL,      # 38
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 39
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 40
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 41
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 42
   ID_EKEB,                ID_NULL,    ID_NULL,      # 43
   ID_REEH,                ID_NULL,    ID_NULL,      # 44
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 45
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 46
   ID_KITABO,              ID_NULL,    ID_NULL,      # 47
   ID_NITSABIM,            ID_VAYELEH, ID_NULL,      # 48
   ID_ROSH_HASHANAH_I,     ID_NULL,    ID_NULL,      # 49
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 50
   ID_SUCCOTH_I,           ID_NULL,    ID_NULL,      # 51
   ID_SHEMINI_AZERETH,     ID_NULL,    ID_NULL       # 52
  ]

torahSectionsCIsrael = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_SHEKALIM,ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_ZAHOR,   ID_NULL,      # 20
   ID_KITISSA,             ID_PARAH,   ID_NULL,      # 21
   ID_VAYAKHEL,            ID_PEKUDE,  ID_HAHODESH,  # 22
   ID_VAYIKRA,             ID_NULL,    ID_NULL,      # 24
   ID_TSAV,                ID_HAGGADOL,ID_NULL,      # 25
   ID_HOL_HAMOED_PESAH,    ID_NULL,    ID_NULL,      # 26
   ID_SHEMINI,             ID_NULL,    ID_NULL,      # 27
   ID_TAZRIANG,           ID_METSORANG,ID_NULL,      # 28
   ID_AHAREMOTH,           ID_KEDOSHIM,ID_NULL,      # 29
   ID_EMOR,                ID_NULL,    ID_NULL,      # 30
   ID_BEHAR,            ID_BEHUKKOTHAI,ID_NULL,      # 31
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 32
   ID_NASO,                ID_NULL,    ID_NULL,      # 33
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 34
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 35
   ID_KORAH,               ID_NULL,    ID_NULL,      # 36
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 37
   ID_BALAK,               ID_NULL,    ID_NULL,      # 38
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 39
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 40
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 41
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 42
   ID_EKEB,                ID_NULL,    ID_NULL,      # 43
   ID_REEH,                ID_NULL,    ID_NULL,      # 44
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 45
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 46
   ID_KITABO,              ID_NULL,    ID_NULL,      # 47
   ID_NITSABIM,            ID_VAYELEH, ID_NULL,      # 48
   ID_ROSH_HASHANAH_I,     ID_NULL,    ID_NULL,      # 49
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 50
   ID_SUCCOTH_I,           ID_NULL,    ID_NULL,      # 51
   ID_SHEMINI_AZERETH,     ID_NULL,    ID_NULL]     # 52

torahSectionsDDiaspora = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_SHEKALIM,ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_ZAHOR,   ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_PEKUDE,  ID_PARAH,     # 22
   ID_VAYIKRA,             ID_HAHODESH,ID_NULL,      # 23
   ID_TSAV,                ID_HAGGADOL,ID_NULL,      # 24
   ID_PESAH_I,             ID_NULL,    ID_NULL,      # 25
   ID_PESAH_VIII,          ID_NULL,    ID_NULL,      # 26
   ID_SHEMINI,             ID_NULL,    ID_NULL,      # 27
   ID_TAZRIANG,           ID_METSORANG,ID_NULL,      # 28
   ID_AHAREMOTH,           ID_KEDOSHIM,ID_NULL,      # 29
   ID_EMOR,                ID_NULL,    ID_NULL,      # 30
   ID_BEHAR,            ID_BEHUKKOTHAI,ID_NULL,      # 31
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 32
   ID_NASO,                ID_NULL,    ID_NULL,      # 33
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 34
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 35
   ID_KORAH,               ID_NULL,    ID_NULL,      # 36
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 37
   ID_BALAK,               ID_NULL,    ID_NULL,      # 38
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 39
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 40
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 41
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 42
   ID_EKEB,                ID_NULL,    ID_NULL,      # 43
   ID_REEH,                ID_NULL,    ID_NULL,      # 44
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 45
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 46
   ID_KITABO,              ID_NULL,    ID_NULL,      # 47
   ID_NITSABIM,            ID_NULL,    ID_NULL,      # 48
   ID_VAYELEH,             ID_NULL,    ID_NULL,      # 49
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 50
   ID_HOL_HAMOED_SUCCOTH,  ID_NULL,    ID_NULL]     # 51

torahSectionsDIsrael = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_SHEKALIM,ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_ZAHOR,   ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_PEKUDE,  ID_PARAH,     # 22
   ID_VAYIKRA,             ID_HAHODESH,ID_NULL,      # 23
   ID_TSAV,                ID_HAGGADOL,ID_NULL,      # 24
   ID_PESAH_I,             ID_NULL,    ID_NULL,      # 25
   ID_SHEMINI,             ID_NULL,    ID_NULL,      # 26
   ID_TAZRIANG,           ID_METSORANG,ID_NULL,      # 27
   ID_AHAREMOTH,           ID_KEDOSHIM,ID_NULL,      # 28
   ID_EMOR,                ID_NULL,    ID_NULL,      # 29
   ID_BEHAR,               ID_NULL,    ID_NULL,      # 30
   ID_BEHUKKOTHAI,         ID_NULL,    ID_NULL,      # 31
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 32
   ID_NASO,                ID_NULL,    ID_NULL,      # 33
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 34
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 35
   ID_KORAH,               ID_NULL,    ID_NULL,      # 36
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 37
   ID_BALAK,               ID_NULL,    ID_NULL,      # 38
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 39
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 40
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 41
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 42
   ID_EKEB,                ID_NULL,    ID_NULL,      # 43
   ID_REEH,                ID_NULL,    ID_NULL,      # 44
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 45
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 46
   ID_KITABO,              ID_NULL,    ID_NULL,      # 47
   ID_NITSABIM,            ID_NULL,    ID_NULL,      # 48
   ID_VAYELEH,             ID_NULL,    ID_NULL,      # 49
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 50
   ID_HOL_HAMOED_SUCCOTH,  ID_NULL,    ID_NULL]     # 51

torahSectionsEDiaspora = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_SHEKALIM,ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_ZAHOR,   ID_NULL,      # 20
   ID_KITISSA,             ID_PARAH,   ID_NULL,      # 21
   ID_VAYAKHEL,            ID_PEKUDE,  ID_HAHODESH,  # 22
   ID_VAYIKRA,             ID_NULL,    ID_NULL,      # 23
   ID_TSAV,                ID_HAGGADOL,ID_NULL,      # 24
   ID_HOL_HAMOED_PESAH,    ID_NULL,    ID_NULL,      # 26
   ID_SHEMINI,             ID_NULL,    ID_NULL,      # 27
   ID_TAZRIANG,           ID_METSORANG,ID_NULL,      # 28
   ID_AHAREMOTH,           ID_KEDOSHIM,ID_NULL,      # 29
   ID_EMOR,                ID_NULL,    ID_NULL,      # 30
   ID_BEHAR,            ID_BEHUKKOTHAI,ID_NULL,      # 31
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 32
   ID_SHAVUOTH_II,         ID_NULL,    ID_NULL,      # 33
   ID_NASO,                ID_NULL,    ID_NULL,      # 34
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 35
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 36
   ID_KORAH,               ID_NULL,    ID_NULL,      # 37
   ID_HUKATH,              ID_BALAK,   ID_NULL,      # 38
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 39
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 40
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 41
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 42
   ID_EKEB,                ID_NULL,    ID_NULL,      # 43
   ID_REEH,                ID_NULL,    ID_NULL,      # 44
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 45
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 46
   ID_KITABO,              ID_NULL,    ID_NULL,      # 47
   ID_NITSABIM,            ID_VAYELEH, ID_NULL,      # 48
   ID_ROSH_HASHANAH_I,     ID_NULL,    ID_NULL,      # 49
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 50
   ID_SUCCOTH_I,           ID_NULL,    ID_NULL,      # 51
   ID_SHEMINI_AZERETH,     ID_NULL,    ID_NULL]     # 52

torahSectionsEIsrael = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_SHEKALIM,ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_ZAHOR,   ID_NULL,      # 20
   ID_KITISSA,             ID_PARAH,   ID_NULL,      # 21
   ID_VAYAKHEL,            ID_PEKUDE,  ID_HAHODESH,  # 22
   ID_VAYIKRA,             ID_NULL,    ID_NULL,      # 23
   ID_TSAV,                ID_HAGGADOL,ID_NULL,      # 24
   ID_HOL_HAMOED_PESAH,    ID_NULL,    ID_NULL,      # 26
   ID_SHEMINI,             ID_NULL,    ID_NULL,      # 27
   ID_TAZRIANG,           ID_METSORANG,ID_NULL,      # 28
   ID_AHAREMOTH,           ID_KEDOSHIM,ID_NULL,      # 29
   ID_EMOR,                ID_NULL,    ID_NULL,      # 30
   ID_BEHAR,            ID_BEHUKKOTHAI,ID_NULL,      # 31
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 32
   ID_SHAVUOTH_II,         ID_NULL,    ID_NULL,      # 33
   ID_NASO,                ID_NULL,    ID_NULL,      # 34
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 35
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 36
   ID_KORAH,               ID_NULL,    ID_NULL,      # 37
   ID_HUKATH,              ID_BALAK,   ID_NULL,      # 38
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 39
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 40
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 41
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 42
   ID_EKEB,                ID_NULL,    ID_NULL,      # 43
   ID_REEH,                ID_NULL,    ID_NULL,      # 44
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 45
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 46
   ID_KITABO,              ID_NULL,    ID_NULL,      # 47
   ID_NITSABIM,            ID_VAYELEH, ID_NULL,      # 48
   ID_ROSH_HASHANAH_I,     ID_NULL,    ID_NULL,      # 49
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 50
   ID_SUCCOTH_I,           ID_NULL,    ID_NULL,      # 51
   ID_SHEMINI_AZERETH,     ID_NULL,    ID_NULL]     # 52

torahSectionsF = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_NULL,    ID_NULL,      # 18
   ID_TERUMAH,             ID_SHEKALIM,ID_NULL,      # 19
   ID_TETSAVVEH,           ID_ZAHOR,   ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_PARAH,   ID_NULL,      # 22
   ID_PEKUDE,              ID_HAHODESH,ID_NULL,      # 23
   ID_VAYIKRA,             ID_NULL,    ID_NULL,      # 24
   ID_TSAV,                ID_HAGGADOL,ID_NULL,      # 25
   ID_PESAH_VII,           ID_NULL,    ID_NULL,      # 26
   ID_SHEMINI,             ID_NULL,    ID_NULL,      # 27
   ID_TAZRIANG,           ID_METSORANG,ID_NULL,      # 28
   ID_AHAREMOTH,           ID_KEDOSHIM,ID_NULL,      # 29
   ID_EMOR,                ID_NULL,    ID_NULL,      # 30
   ID_BEHAR,            ID_BEHUKKOTHAI,ID_NULL,      # 31
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 32
   ID_NASO,                ID_NULL,    ID_NULL,      # 34
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 35
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 36
   ID_KORAH,               ID_NULL,    ID_NULL,      # 37
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 38
   ID_BALAK,               ID_NULL,    ID_NULL,      # 39
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 40
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 41
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 42
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 43
   ID_EKEB,                ID_NULL,    ID_NULL,      # 44
   ID_REEH,                ID_NULL,    ID_NULL,      # 45
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 46
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 47
   ID_KITABO,              ID_NULL,    ID_NULL,      # 48
   ID_NITSABIM,            ID_NULL,    ID_NULL,      # 49
   ID_VAYELEH,             ID_NULL,    ID_NULL,      # 50
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 51
   ID_HOL_HAMOED_SUCCOTH,  ID_NULL,    ID_NULL]     # 52

torahSectionsG = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_SHEKALIM,ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_ZAHOR,   ID_NULL,      # 20
   ID_KITISSA,             ID_PARAH,   ID_NULL,      # 21
   ID_VAYAKHEL,            ID_PEKUDE,  ID_HAHODESH,  # 22
   ID_VAYIKRA,             ID_NULL,    ID_NULL,      # 24
   ID_TSAV,                ID_HAGGADOL,ID_NULL,      # 25
   ID_HOL_HAMOED_PESAH,    ID_NULL,    ID_NULL,      # 26
   ID_SHEMINI,             ID_NULL,    ID_NULL,      # 27
   ID_TAZRIANG,           ID_METSORANG,ID_NULL,      # 28
   ID_AHAREMOTH,           ID_KEDOSHIM,ID_NULL,      # 29
   ID_EMOR,                ID_NULL,    ID_NULL,      # 30
   ID_BEHAR,            ID_BEHUKKOTHAI,ID_NULL,      # 31
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 32
   ID_NASO,                ID_NULL,    ID_NULL,      # 33
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 34
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 35
   ID_KORAH,               ID_NULL,    ID_NULL,      # 36
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 37
   ID_BALAK,               ID_NULL,    ID_NULL,      # 38
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 39
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 40
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 41
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 42
   ID_EKEB,                ID_NULL,    ID_NULL,      # 43
   ID_REEH,                ID_NULL,    ID_NULL,      # 44
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 45
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 46
   ID_KITABO,              ID_NULL,    ID_NULL,      # 47
   ID_NITSABIM,            ID_VAYELEH, ID_NULL,      # 48
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 49
   ID_YOM_KIPPUR,          ID_NULL,    ID_NULL,      # 50
   ID_HOL_HAMOED_SUCCOTH,  ID_NULL,    ID_NULL]     # 51

torahSectionsHDiaspora = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_NULL,    ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_NULL,    ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_SHEKALIM,ID_NULL,      # 22
   ID_PEKUDE,              ID_NULL,    ID_NULL,      # 23
   ID_VAYIKRA,             ID_ZAHOR,   ID_NULL,      # 24
   ID_TSAV,                ID_PARAH,   ID_NULL,      # 25
   ID_SHEMINI,             ID_HAHODESH,ID_NULL,      # 26
   ID_TAZRIANG,            ID_NULL,    ID_NULL,      # 27
   ID_METSORANG,           ID_HAGGADOL,ID_NULL,      # 28
   ID_HOL_HAMOED_PESAH,    ID_NULL,    ID_NULL,      # 29
   ID_AHAREMOTH,           ID_NULL,    ID_NULL,      # 30
   ID_KEDOSHIM,            ID_NULL,    ID_NULL,      # 31
   ID_EMOR,                ID_NULL,    ID_NULL,      # 32
   ID_BEHAR,               ID_NULL,    ID_NULL,      # 33
   ID_BEHUKKOTHAI,         ID_NULL,    ID_NULL,      # 34
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 35
   ID_SHAVUOTH_II,         ID_NULL,    ID_NULL,      # 36
   ID_NASO,                ID_NULL,    ID_NULL,      # 37
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 38
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 39
   ID_KORAH,               ID_NULL,    ID_NULL,      # 40
   ID_HUKATH,              ID_BALAK,   ID_NULL,      # 41
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 42
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 43
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 44
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 45
   ID_EKEB,                ID_NULL,    ID_NULL,      # 46
   ID_REEH,                ID_NULL,    ID_NULL,      # 47
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 48
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 49
   ID_KITABO,              ID_NULL,    ID_NULL,      # 50
   ID_NITSABIM,            ID_VAYELEH, ID_NULL,      # 51
   ID_ROSH_HASHANAH_I,     ID_NULL,    ID_NULL,      # 52
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 53
   ID_SUCCOTH_I,           ID_NULL,    ID_NULL,      # 54
   ID_SHEMINI_AZERETH,     ID_NULL,    ID_NULL]     # 55

torahSectionsHIsrael = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_NULL,    ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_NULL,    ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_SHEKALIM,ID_NULL,      # 22
   ID_PEKUDE,              ID_NULL,    ID_NULL,      # 23
   ID_VAYIKRA,             ID_ZAHOR,   ID_NULL,      # 24
   ID_TSAV,                ID_PARAH,   ID_NULL,      # 25
   ID_SHEMINI,             ID_HAHODESH,ID_NULL,      # 26
   ID_TAZRIANG,            ID_NULL,    ID_NULL,      # 27
   ID_METSORANG,           ID_HAGGADOL,ID_NULL,      # 28
   ID_HOL_HAMOED_PESAH,    ID_NULL,    ID_NULL,      # 29
   ID_AHAREMOTH,           ID_NULL,    ID_NULL,      # 30
   ID_KEDOSHIM,            ID_NULL,    ID_NULL,      # 31
   ID_EMOR,                ID_NULL,    ID_NULL,      # 32
   ID_BEHAR,               ID_NULL,    ID_NULL,      # 33
   ID_BEHUKKOTHAI,         ID_NULL,    ID_NULL,      # 34
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 35
   ID_NASO,                ID_NULL,    ID_NULL,      # 36
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 37
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 38
   ID_KORAH,               ID_NULL,    ID_NULL,      # 39
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 40
   ID_BALAK,               ID_NULL,    ID_NULL,      # 41
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 42
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 43
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 44
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 45
   ID_EKEB,                ID_NULL,    ID_NULL,      # 46
   ID_REEH,                ID_NULL,    ID_NULL,      # 47
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 48
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 49
   ID_KITABO,              ID_NULL,    ID_NULL,      # 50
   ID_NITSABIM,            ID_VAYELEH, ID_NULL,      # 51
   ID_ROSH_HASHANAH_I,     ID_NULL,    ID_NULL,      # 52
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 53
   ID_SUCCOTH_I,           ID_NULL,    ID_NULL,      # 54
   ID_SHEMINI_AZERETH,     ID_NULL,    ID_NULL]     # 55

torahSectionsI = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_NULL,    ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_NULL,    ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_NULL,    ID_NULL,      # 22
   ID_PEKUDE,              ID_SHEKALIM,ID_NULL,      # 23
   ID_VAYIKRA,             ID_ZAHOR,   ID_NULL,      # 24
   ID_TSAV,                ID_NULL,    ID_NULL,      # 25
   ID_SHEMINI,             ID_PARAH,   ID_NULL,      # 26
   ID_TAZRIANG,            ID_HAHODESH,ID_NULL,      # 27
   ID_METSORANG,           ID_NULL,    ID_NULL,      # 28
   ID_AHAREMOTH,           ID_HAGGADOL,ID_NULL,      # 29
   ID_PESAH_VII,           ID_NULL,    ID_NULL,      # 30
   ID_KEDOSHIM,            ID_NULL,    ID_NULL,      # 31
   ID_EMOR,                ID_NULL,    ID_NULL,      # 32
   ID_BEHAR,               ID_NULL,    ID_NULL,      # 33
   ID_BEHUKKOTHAI,         ID_NULL,    ID_NULL,      # 34
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 35
   ID_NASO,                ID_NULL,    ID_NULL,      # 36
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 37
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 38
   ID_KORAH,               ID_NULL,    ID_NULL,      # 39
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 40
   ID_BALAK,               ID_NULL,    ID_NULL,      # 41
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 42
   ID_MATOTH,              ID_NULL,    ID_NULL,      # 43
   ID_MASEH,               ID_NULL,    ID_NULL,      # 44
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 45
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 46
   ID_EKEB,                ID_NULL,    ID_NULL,      # 47
   ID_REEH,                ID_NULL,    ID_NULL,      # 48
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 49
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 50
   ID_KITABO,              ID_NULL,    ID_NULL,      # 51
   ID_NITSABIM,            ID_NULL,    ID_NULL,      # 52
   ID_VAYELEH,             ID_NULL,    ID_NULL,      # 53
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 54
   ID_HOL_HAMOED_SUCCOTH,  ID_NULL,    ID_NULL]     # 55

torahSectionsJ = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_NULL,    ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_NULL,    ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_SHEKALIM,ID_NULL,      # 22
   ID_PEKUDE,              ID_NULL,    ID_NULL,      # 23
   ID_VAYIKRA,             ID_ZAHOR,   ID_NULL,      # 24
   ID_TSAV,                ID_PARAH,   ID_NULL,      # 25
   ID_SHEMINI,             ID_HAHODESH,ID_NULL,      # 26
   ID_TAZRIANG,            ID_NULL,    ID_NULL,      # 27
   ID_METSORANG,           ID_HAGGADOL,ID_NULL,      # 28
   ID_HOL_HAMOED_PESAH,    ID_NULL,    ID_NULL,      # 29
   ID_AHAREMOTH,           ID_NULL,    ID_NULL,      # 30
   ID_KEDOSHIM,            ID_NULL,    ID_NULL,      # 31
   ID_EMOR,                ID_NULL,    ID_NULL,      # 32
   ID_BEHAR,               ID_NULL,    ID_NULL,      # 33
   ID_BEHUKKOTHAI,         ID_NULL,    ID_NULL,      # 34
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 35
   ID_NASO,                ID_NULL,    ID_NULL,      # 36
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 37
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 38
   ID_KORAH,               ID_NULL,    ID_NULL,      # 39
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 40
   ID_BALAK,               ID_NULL,    ID_NULL,      # 41
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 42
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 43
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 44
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 45
   ID_EKEB,                ID_NULL,    ID_NULL,      # 46
   ID_REEH,                ID_NULL,    ID_NULL,      # 47
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 48
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 49
   ID_KITABO,              ID_NULL,    ID_NULL,      # 50
   ID_NITSABIM,            ID_VAYELEH, ID_NULL,      # 51
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 52
   ID_YOM_KIPPUR,          ID_NULL,    ID_NULL,      # 53
   ID_HOL_HAMOED_SUCCOTH,  ID_NULL,    ID_NULL]     # 54

torahSectionsKDiaspora = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_NULL,    ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_NULL,    ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_SHEKALIM,ID_NULL,      # 22
   ID_PEKUDE,              ID_NULL,    ID_NULL,      # 23
   ID_VAYIKRA,             ID_ZAHOR,   ID_NULL,      # 24
   ID_TSAV,                ID_NULL,    ID_NULL,      # 25
   ID_SHEMINI,             ID_PARAH,   ID_NULL,      # 26
   ID_TAZRIANG,            ID_HAHODESH,ID_NULL,      # 27
   ID_METSORANG,           ID_HAGGADOL,ID_NULL,      # 28
   ID_PESAH_I,             ID_NULL,    ID_NULL,      # 29
   ID_PESAH_VIII,          ID_NULL,    ID_NULL,      # 30
   ID_AHAREMOTH,           ID_NULL,    ID_NULL,      # 31
   ID_KEDOSHIM,            ID_NULL,    ID_NULL,      # 32
   ID_EMOR,                ID_NULL,    ID_NULL,      # 33
   ID_BEHAR,               ID_NULL,    ID_NULL,      # 34
   ID_BEHUKKOTHAI,         ID_NULL,    ID_NULL,      # 35
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 36
   ID_NASO,                ID_NULL,    ID_NULL,      # 37
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 38
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 39
   ID_KORAH,               ID_NULL,    ID_NULL,      # 40
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 41
   ID_BALAK,               ID_NULL,    ID_NULL,      # 42
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 43
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 44
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 45
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 46
   ID_EKEB,                ID_NULL,    ID_NULL,      # 47
   ID_REEH,                ID_NULL,    ID_NULL,      # 48
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 49
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 50
   ID_KITABO,              ID_NULL,    ID_NULL,      # 51
   ID_NITSABIM,            ID_NULL,    ID_NULL,      # 52
   ID_VAYELEH,             ID_NULL,    ID_NULL,      # 53
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 54
   ID_HOL_HAMOED_SUCCOTH,  ID_NULL,    ID_NULL]     # 55

torahSectionsKIsrael = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_NULL,    ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_NULL,    ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_SHEKALIM,ID_NULL,      # 22
   ID_PEKUDE,              ID_NULL,    ID_NULL,      # 23
   ID_VAYIKRA,             ID_ZAHOR,   ID_NULL,      # 24
   ID_TSAV,                ID_NULL,    ID_NULL,      # 25
   ID_SHEMINI,             ID_PARAH,   ID_NULL,      # 26
   ID_TAZRIANG,            ID_HAHODESH,ID_NULL,      # 27
   ID_METSORANG,           ID_HAGGADOL,ID_NULL,      # 28
   ID_PESAH_I,             ID_NULL,    ID_NULL,      # 29
   ID_AHAREMOTH,           ID_NULL,    ID_NULL,      # 30
   ID_KEDOSHIM,            ID_NULL,    ID_NULL,      # 31
   ID_EMOR,                ID_NULL,    ID_NULL,      # 32
   ID_BEHAR,               ID_NULL,    ID_NULL,      # 33
   ID_BEHUKKOTHAI,         ID_NULL,    ID_NULL,      # 34
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 35
   ID_NASO,                ID_NULL,    ID_NULL,      # 36
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 37
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 38
   ID_KORAH,               ID_NULL,    ID_NULL,      # 39
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 40
   ID_BALAK,               ID_NULL,    ID_NULL,      # 41
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 42
   ID_MATOTH,              ID_NULL,    ID_NULL,      # 43
   ID_MASEH,               ID_NULL,    ID_NULL,      # 44
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 45
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 46
   ID_EKEB,                ID_NULL,    ID_NULL,      # 47
   ID_REEH,                ID_NULL,    ID_NULL,      # 48
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 49
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 50
   ID_KITABO,              ID_NULL,    ID_NULL,      # 51
   ID_NITSABIM,            ID_NULL,    ID_NULL,      # 52
   ID_VAYELEH,             ID_NULL,    ID_NULL,      # 53
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 54
   ID_HOL_HAMOED_SUCCOTH,  ID_NULL,    ID_NULL]     # 55

torahSectionsLDiaspora = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_NULL,    ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_NULL,    ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_SHEKALIM,ID_NULL,      # 22
   ID_PEKUDE,              ID_NULL,    ID_NULL,      # 23
   ID_VAYIKRA,             ID_ZAHOR,  ID_NULL,      # 24
   ID_TSAV,                ID_NULL,    ID_NULL,      # 25
   ID_SHEMINI,             ID_PARAH,   ID_NULL,      # 26
   ID_TAZRIANG,            ID_HAHODESH,ID_NULL,      # 27
   ID_METSORANG,           ID_HAGGADOL,ID_NULL,      # 28
   ID_PESAH_I,             ID_NULL,    ID_NULL,      # 29
   ID_PESAH_VIII,          ID_NULL,    ID_NULL,      # 30
   ID_AHAREMOTH,           ID_NULL,    ID_NULL,      # 31
   ID_KEDOSHIM,            ID_NULL,    ID_NULL,      # 32
   ID_EMOR,                ID_NULL,    ID_NULL,      # 33
   ID_BEHAR,               ID_NULL,    ID_NULL,      # 34
   ID_BEHUKKOTHAI,         ID_NULL,    ID_NULL,      # 35
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 36
   ID_NASO,                ID_NULL,    ID_NULL,      # 37
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 38
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 39
   ID_KORAH,               ID_NULL,    ID_NULL,      # 40
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 41
   ID_BALAK,               ID_NULL,    ID_NULL,      # 42
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 43
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 44
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 45
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 46
   ID_EKEB,                ID_NULL,    ID_NULL,      # 47
   ID_REEH,                ID_NULL,    ID_NULL,      # 48
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 49
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 50
   ID_KITABO,              ID_NULL,    ID_NULL,      # 51
   ID_NITSABIM,            ID_NULL,    ID_NULL,      # 52
   ID_VAYELEH,             ID_NULL,    ID_NULL,      # 53
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 54
   ID_HOL_HAMOED_SUCCOTH,  ID_NULL,    ID_NULL]     # 55

torahSectionsLIsrael = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_NULL,    ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_NULL,    ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_SHEKALIM,ID_NULL,      # 22
   ID_PEKUDE,              ID_NULL,    ID_NULL,      # 23
   ID_VAYIKRA,             ID_ZAHOR,  ID_NULL,      # 24
   ID_TSAV,                ID_NULL,    ID_NULL,      # 25
   ID_SHEMINI,             ID_PARAH,   ID_NULL,      # 26
   ID_TAZRIANG,            ID_HAHODESH,ID_NULL,      # 27
   ID_METSORANG,           ID_HAGGADOL,ID_NULL,      # 28
   ID_PESAH_I,             ID_NULL,    ID_NULL,      # 29
   ID_AHAREMOTH,           ID_NULL,    ID_NULL,      # 30
   ID_KEDOSHIM,            ID_NULL,    ID_NULL,      # 31
   ID_EMOR,                ID_NULL,    ID_NULL,      # 32
   ID_BEHAR,               ID_NULL,    ID_NULL,      # 33
   ID_BEHUKKOTHAI,         ID_NULL,    ID_NULL,      # 34
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 35
   ID_NASO,                ID_NULL,    ID_NULL,      # 36
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 37
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 38
   ID_KORAH,               ID_NULL,    ID_NULL,      # 39
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 40
   ID_BALAK,               ID_NULL,    ID_NULL,      # 41
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 42
   ID_MATOTH,              ID_NULL,    ID_NULL,      # 43
   ID_MASEH,               ID_NULL,    ID_NULL,      # 44
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 45
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 46
   ID_EKEB,                ID_NULL,    ID_NULL,      # 47
   ID_REEH,                ID_NULL,    ID_NULL,      # 48
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 49
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 50
   ID_KITABO,              ID_NULL,    ID_NULL,      # 51
   ID_NITSABIM,            ID_NULL,    ID_NULL,      # 52
   ID_VAYELEH,             ID_NULL,    ID_NULL,      # 53
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 54
   ID_HOL_HAMOED_SUCCOTH,  ID_NULL,    ID_NULL]     # 55

torahSectionsM = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_NULL,    ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_NULL,    ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_NULL,    ID_NULL,      # 22
   ID_PEKUDE,              ID_SHEKALIM,ID_NULL,      # 23
   ID_VAYIKRA,             ID_NULL,    ID_NULL,      # 24
   ID_TSAV,                ID_ZAHOR,   ID_NULL,      # 25
   ID_SHEMINI,             ID_PARAH,   ID_NULL,      # 26
   ID_TAZRIANG,            ID_HAHODESH,ID_NULL,      # 27
   ID_METSORANG,           ID_NULL,    ID_NULL,      # 28
   ID_AHAREMOTH,           ID_HAGGADOL,ID_NULL,      # 29
   ID_HOL_HAMOED_PESAH,    ID_NULL,    ID_NULL,      # 30
   ID_KEDOSHIM,            ID_NULL,    ID_NULL,      # 31
   ID_EMOR,                ID_NULL,    ID_NULL,      # 32
   ID_BEHAR,               ID_NULL,    ID_NULL,      # 33
   ID_BEHUKKOTHAI,         ID_NULL,    ID_NULL,      # 34
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 35
   ID_NASO,                ID_NULL,    ID_NULL,      # 36
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 37
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 38
   ID_KORAH,               ID_NULL,    ID_NULL,      # 39
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 40
   ID_BALAK,               ID_NULL,    ID_NULL,      # 41
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 42
   ID_MATOTH,              ID_NULL,    ID_NULL,      # 43
   ID_MASEH,               ID_NULL,    ID_NULL,      # 44
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 45
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 46
   ID_EKEB,                ID_NULL,    ID_NULL,      # 47
   ID_REEH,                ID_NULL,    ID_NULL,      # 48
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 49
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 50
   ID_KITABO,              ID_NULL,    ID_NULL,      # 51
   ID_NITSABIM,            ID_VAYELEH, ID_NULL,      # 52
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 53
   ID_YOM_KIPPUR,          ID_NULL,    ID_NULL,      # 54
   ID_HOL_HAMOED_SUCCOTH,  ID_NULL,    ID_NULL]     # 55

torahSectionsNDiaspora = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_NULL,    ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_NULL,    ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_SHEKALIM,ID_NULL,      # 22
   ID_PEKUDE,              ID_NULL,    ID_NULL,      # 23
   ID_VAYIKRA,             ID_ZAHOR,   ID_NULL,      # 24
   ID_TSAV,                ID_PARAH,   ID_NULL,      # 25
   ID_SHEMINI,             ID_HAHODESH,ID_NULL,      # 26
   ID_TAZRIANG,            ID_NULL,    ID_NULL,      # 27
   ID_METSORANG,           ID_HAGGADOL,ID_NULL,      # 28
   ID_HOL_HAMOED_PESAH,    ID_NULL,    ID_NULL,      # 29
   ID_AHAREMOTH,           ID_NULL,    ID_NULL,      # 30
   ID_KEDOSHIM,            ID_NULL,    ID_NULL,      # 31
   ID_EMOR,                ID_NULL,    ID_NULL,      # 32
   ID_BEHAR,               ID_NULL,    ID_NULL,      # 33
   ID_BEHUKKOTHAI,         ID_NULL,    ID_NULL,      # 34
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 35
   ID_SHAVUOTH_II,         ID_NULL,    ID_NULL,      # 36
   ID_NASO,                ID_NULL,    ID_NULL,      # 37
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 38
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 39
   ID_KORAH,               ID_NULL,    ID_NULL,      # 40
   ID_HUKATH,              ID_BALAK,   ID_NULL,      # 41
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 42
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 43
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 44
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 45
   ID_EKEB,                ID_NULL,    ID_NULL,      # 46
   ID_REEH,                ID_NULL,    ID_NULL,      # 47
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 48
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 49
   ID_KITABO,              ID_NULL,    ID_NULL,      # 50
   ID_NITSABIM,            ID_VAYELEH, ID_NULL,      # 51
   ID_ROSH_HASHANAH_I,     ID_NULL,    ID_NULL,      # 52
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 53
   ID_SUCCOTH_I,           ID_NULL,    ID_NULL,      # 54
   ID_SHEMINI_AZERETH,     ID_NULL,    ID_NULL]     # 55

torahSectionsNIsrael = \
  [ID_BERESHITH,           ID_NULL,    ID_NULL,      #  1
   ID_NOAH,                ID_NULL,    ID_NULL,      #  2
   ID_LEHLEHA,             ID_NULL,    ID_NULL,      #  3
   ID_VAYERA,              ID_NULL,    ID_NULL,      #  4
   ID_HAYESARAH,           ID_NULL,    ID_NULL,      #  5
   ID_TOLEDOTH,            ID_NULL,    ID_NULL,      #  6
   ID_VAYETSE,             ID_NULL,    ID_NULL,      #  7
   ID_VAYISHLAH,           ID_NULL,    ID_NULL,      #  8
   ID_VAYESHEB,            ID_NULL,    ID_NULL,      #  9
   ID_MIKKETS,             ID_NULL,    ID_NULL,      # 10
   ID_VAYIGGASH,           ID_NULL,    ID_NULL,      # 11
   ID_VAYHEE,              ID_NULL,    ID_NULL,      # 12
   ID_SHEMOTH,             ID_NULL,    ID_NULL,      # 13
   ID_VAERA,               ID_NULL,    ID_NULL,      # 14
   ID_BO,                  ID_NULL,    ID_NULL,      # 15
   ID_BESHALLAH,           ID_NULL,    ID_NULL,      # 16
   ID_YITHRO,              ID_NULL,    ID_NULL,      # 17
   ID_MISHPATIM,           ID_NULL,    ID_NULL,      # 18
   ID_TERUMAH,             ID_NULL,    ID_NULL,      # 19
   ID_TETSAVVEH,           ID_NULL,    ID_NULL,      # 20
   ID_KITISSA,             ID_NULL,    ID_NULL,      # 21
   ID_VAYAKHEL,            ID_SHEKALIM,ID_NULL,      # 22
   ID_PEKUDE,              ID_NULL,    ID_NULL,      # 23
   ID_VAYIKRA,             ID_ZAHOR,   ID_NULL,      # 24
   ID_TSAV,                ID_PARAH,   ID_NULL,      # 25
   ID_SHEMINI,             ID_HAHODESH,ID_NULL,      # 26
   ID_TAZRIANG,            ID_NULL,    ID_NULL,      # 27
   ID_METSORANG,           ID_HAGGADOL,ID_NULL,      # 28
   ID_HOL_HAMOED_PESAH,    ID_NULL,    ID_NULL,      # 29
   ID_AHAREMOTH,           ID_NULL,    ID_NULL,      # 30
   ID_KEDOSHIM,            ID_NULL,    ID_NULL,      # 31
   ID_EMOR,                ID_NULL,    ID_NULL,      # 32
   ID_BEHAR,               ID_NULL,    ID_NULL,      # 33
   ID_BEHUKKOTHAI,         ID_NULL,    ID_NULL,      # 34
   ID_BEMIDBAR,            ID_NULL,    ID_NULL,      # 35
   ID_NASO,                ID_NULL,    ID_NULL,      # 36
   ID_BEHAALOTEHA,         ID_NULL,    ID_NULL,      # 37
   ID_SHELAHLEHA,          ID_NULL,    ID_NULL,      # 38
   ID_KORAH,               ID_NULL,    ID_NULL,      # 39
   ID_HUKATH,              ID_NULL,    ID_NULL,      # 40
   ID_BALAK,               ID_NULL,    ID_NULL,      # 41
   ID_PINHAS,              ID_NULL,    ID_NULL,      # 42
   ID_MATOTH,              ID_MASEH,   ID_NULL,      # 43
   ID_DEBARIM,             ID_NULL,    ID_NULL,      # 44
   ID_VAETHANAN,           ID_NULL,    ID_NULL,      # 45
   ID_EKEB,                ID_NULL,    ID_NULL,      # 46
   ID_REEH,                ID_NULL,    ID_NULL,      # 47
   ID_SHOFETIM,            ID_NULL,    ID_NULL,      # 48
   ID_KITETSE,             ID_NULL,    ID_NULL,      # 49
   ID_KITABO,              ID_NULL,    ID_NULL,      # 50
   ID_NITSABIM,            ID_VAYELEH, ID_NULL,      # 51
   ID_ROSH_HASHANAH_I,     ID_NULL,    ID_NULL,      # 52
   ID_HAAZINU,             ID_NULL,    ID_NULL,      # 53
   ID_SUCCOTH_I,           ID_NULL,    ID_NULL,      # 54
   ID_SHEMINI_AZERETH,     ID_NULL,    ID_NULL]     # 55

def torahGetWeekday(absDate):
  wochentag = (int(absDate) + 2) % 7
  return wochentag

def torahHebrewLeapYear(year):
  return calendar_util.hebrew_leap(year)

def torahLastMonthOfHebrewYear(year):
  return calendar_util.hebrew_year_months(year)

def getYearType(year):
  rhWeekday = torahGetWeekday(calendar_util.hebrew_to_jd(year, 7, 1))
  lengthOfYear = int(calendar_util.hebrew_to_jd(year+1, 7, 1) - calendar_util.hebrew_to_jd(year, 7, 1))
  pesWeekday = torahGetWeekday(calendar_util.hebrew_to_jd(year, 1, 15))

  if ((rhWeekday == 1) and (lengthOfYear == 353) and (pesWeekday == 2)):
    return 1
  if ((rhWeekday == 6) and (lengthOfYear == 353) and (pesWeekday == 0)):
    return 2
  if ((rhWeekday == 2) and (lengthOfYear == 354) and (pesWeekday == 4)):
    return 3
  if ((rhWeekday == 4) and (lengthOfYear == 354) and (pesWeekday == 6)):
    return 4
  if ((rhWeekday == 1) and (lengthOfYear == 355) and (pesWeekday == 4)):
    return 5
  if ((rhWeekday == 4) and (lengthOfYear == 355) and (pesWeekday == 0)):
    return 6
  if ((rhWeekday == 6) and (lengthOfYear == 355) and (pesWeekday == 2)):
    return 7

  if ((rhWeekday == 1) and (lengthOfYear == 383) and (pesWeekday == 4)):
    return 8
  if ((rhWeekday == 4) and (lengthOfYear == 383) and (pesWeekday == 0)):
    return 9
  if ((rhWeekday == 6) and (lengthOfYear == 383) and (pesWeekday == 2)):
    return 10
  if ((rhWeekday == 2) and (lengthOfYear == 384) and (pesWeekday == 6)):
    return 11
  if ((rhWeekday == 1) and (lengthOfYear == 385) and (pesWeekday == 6)):
    return 12
  if ((rhWeekday == 4) and (lengthOfYear == 385) and (pesWeekday == 2)):
    return 13
  if ((rhWeekday == 6) and (lengthOfYear == 385) and (pesWeekday == 4)):
   return 14

  return 0

def determineBereshith(year):
  simchatTorah = calendar_util.hebrew_to_jd(year, 7, 23)
  while (torahGetWeekday(simchatTorah) != 6):
    simchatTorah += 1
  return (simchatTorah)

def getTorahSections(hebrewMonth, hebrewDay, hebrewYear, diaspora):
  shuvahDate = calendar_util.hebrew_to_jd(hebrewYear, 7, 1) + 1
  while (torahGetWeekday(shuvahDate) != 6):
    shuvahDate += 1

  torahDate = calendar_util.hebrew_to_jd(hebrewYear, hebrewMonth, hebrewDay)
  if (torahGetWeekday(torahDate) == 6):
    bereshithDate = determineBereshith(hebrewYear)
    if (torahDate < bereshithDate):
      referenceYear = hebrewYear-1
    else:
      referenceYear = hebrewYear

    yearType = getYearType(referenceYear)
    bereshithDate = determineBereshith(referenceYear)
    torahWeekNo = int(torahDate-bereshithDate)//7

    returnTorahSection = ""
    idTorah1 = ID_NULL
    idTorah2 = ID_NULL
    idTorah3 = ID_NULL
#
# allgemein: A, B, F, G, I, J, M
# Israel/Diaspora: C, D, E, H, K, L, N
#

    if (yearType == 1): # A
      idTorah1 = torahSectionsA[torahWeekNo * 3 + 0]
      idTorah2 = torahSectionsA[torahWeekNo * 3 + 1]
      idTorah3 = torahSectionsA[torahWeekNo * 3 + 2]
    if (yearType == 2): # B
      idTorah1 = torahSectionsB[torahWeekNo * 3 + 0]
      idTorah2 = torahSectionsB[torahWeekNo * 3 + 1]
      idTorah3 = torahSectionsB[torahWeekNo * 3 + 2]
    if (yearType == 3): # C
      if diaspora:
        idTorah1 = torahSectionsCDiaspora[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsCDiaspora[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsCDiaspora[torahWeekNo * 3 + 2]
      else:
        idTorah1 = torahSectionsCIsrael[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsCIsrael[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsCIsrael[torahWeekNo * 3 + 2]
    if (yearType == 4): # D
      if diaspora:
        idTorah1 = torahSectionsDDiaspora[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsDDiaspora[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsDDiaspora[torahWeekNo * 3 + 2]
      else:
        idTorah1 = torahSectionsDIsrael[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsDIsrael[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsDIsrael[torahWeekNo * 3 + 2]
    if (yearType == 5): # E
      if diaspora:
        idTorah1 = torahSectionsEDiaspora[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsEDiaspora[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsEDiaspora[torahWeekNo * 3 + 2]
      else:
        idTorah1 = torahSectionsEIsrael[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsEIsrael[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsEIsrael[torahWeekNo * 3 + 2]
    if (yearType == 6): # F
      idTorah1 = torahSectionsF[torahWeekNo * 3 + 0]
      idTorah2 = torahSectionsF[torahWeekNo * 3 + 1]
      idTorah3 = torahSectionsF[torahWeekNo * 3 + 2]
    if (yearType == 7): # G
      idTorah1 = torahSectionsG[torahWeekNo * 3 + 0]
      idTorah2 = torahSectionsG[torahWeekNo * 3 + 1]
      idTorah3 = torahSectionsG[torahWeekNo * 3 + 2]
    if (yearType == 8): # H
      if diaspora:
        idTorah1 = torahSectionsHDiaspora[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsHDiaspora[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsHDiaspora[torahWeekNo * 3 + 2]
      else:
        idTorah1 = torahSectionsHIsrael[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsHIsrael[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsHIsrael[torahWeekNo * 3 + 2]
    if (yearType == 9): # I
      idTorah1 = torahSectionsI[torahWeekNo * 3 + 0]
      idTorah2 = torahSectionsI[torahWeekNo * 3 + 1]
      idTorah3 = torahSectionsI[torahWeekNo * 3 + 2]
    if (yearType == 10): # J
      idTorah1 = torahSectionsJ[torahWeekNo * 3 + 0]
      idTorah2 = torahSectionsJ[torahWeekNo * 3 + 1]
      idTorah3 = torahSectionsJ[torahWeekNo * 3 + 2]
    if (yearType == 11): # K
      if (diaspora):
        idTorah1 = torahSectionsKDiaspora[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsKDiaspora[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsKDiaspora[torahWeekNo * 3 + 2]
      else:
        idTorah1 = torahSectionsKIsrael[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsKIsrael[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsKIsrael[torahWeekNo * 3 + 2]
    if (yearType == 12): # L
      if (diaspora):
        idTorah1 = torahSectionsLDiaspora[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsLDiaspora[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsLDiaspora[torahWeekNo * 3 + 2]
      else:
        idTorah1 = torahSectionsLIsrael[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsLIsrael[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsLIsrael[torahWeekNo * 3 + 2]
    if (yearType == 13): # M
      idTorah1 = torahSectionsM[torahWeekNo * 3 + 0]
      idTorah2 = torahSectionsM[torahWeekNo * 3 + 1]
      idTorah3 = torahSectionsM[torahWeekNo * 3 + 2]
    if (yearType == 14): # N
      if diaspora:
        idTorah1 = torahSectionsNDiaspora[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsNDiaspora[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsNDiaspora[torahWeekNo * 3 + 2]
      else:
        idTorah1 = torahSectionsNIsrael[torahWeekNo * 3 + 0]
        idTorah2 = torahSectionsNIsrael[torahWeekNo * 3 + 1]
        idTorah3 = torahSectionsNIsrael[torahWeekNo * 3 + 2]

    print('ids:', idTorah1, idTorah2, idTorah3)

    if (idTorah1 != ID_NULL):
      torahSection = getTorahSectionName(idTorah1)
      print('torahSection:', torahSection)
      if (torahSection != ""):
        if (returnTorahSection != ""):
          returnTorahSection = returnTorahSection + ", "
        returnTorahSection = returnTorahSection + torahSection
    if (idTorah2 != ID_NULL):
      torahSection = getTorahSectionName(idTorah2)
      if (torahSection != ""):
        if (returnTorahSection != ""):
          returnTorahSection = returnTorahSection + ", "
        returnTorahSection = returnTorahSection + torahSection
    if (idTorah3 != ID_NULL):
      torahSection = getTorahSectionName(idTorah3)
      if (torahSection != ""):
        if (returnTorahSection != ""):
          returnTorahSection = returnTorahSection + ", "
        returnTorahSection = returnTorahSection + torahSection

    if (torahDate == shuvahDate):
      if (returnTorahSection != ""):
        returnTorahSection = returnTorahSection + ", "
      returnTorahSection = returnTorahSection + getTorahSectionName(ID_SHUVA)

    return (returnTorahSection)
  else:
    return ""

def getTorahSectionName(section):
  if (section == ID_BERESHITH):
    return "Bereshith"
  if (section == ID_NOAH):
    return "Noah"
  if (section == ID_LEHLEHA):
    return "Le'h Leha"
  if (section == ID_VAYERA):
    return "Vayera"
  if (section == ID_HAYESARAH):
    return "Haye Sarah"
  if (section == ID_TOLEDOTH):
    return "Toledoth"
  if (section == ID_VAYETSE):
    return "Vayetse"
  if (section == ID_VAYISHLAH):
    return "Vayishlah"
  if (section == ID_VAYESHEB):
    return "Vayesheb"
  if (section == ID_MIKKETS):
    return "Mikkets"
  if (section == ID_VAYIGGASH):
    return "Vayiggash"
  if (section == ID_VAYHEE):
    return "Vayhee"
  if (section == ID_SHEMOTH):
    return "Shemoth"
  if (section == ID_VAERA):
    return "Vaera"
  if (section == ID_BO):
    return "Bo"
  if (section == ID_BESHALLAH):
    return "Beshallah, Shabbat Shirah"
  if (section == ID_YITHRO):
    return "Yithro"
  if (section == ID_MISHPATIM):
    return "Mishpatim"
  if (section == ID_TERUMAH):
    return "Terumah"
  if (section == ID_TETSAVVEH):
    return "Tetsavveh"
  if (section == ID_KITISSA):
    return "Ki Tissa"
  if (section == ID_VAYAKHEL):
    return "Vayakhel"
  if (section == ID_PEKUDE):
    return "Pekude"
  if (section == ID_VAYIKRA):
    return "Vayikra"
  if (section == ID_TSAV):
    return "Tsav"
  if (section == ID_SHEMINI):
    return "Shemini"
  if (section == ID_TAZRIANG):
    return "Tazria"
  if (section == ID_METSORANG):
    return "Metsora"
  if (section == ID_AHAREMOTH):
    return "Aharemoth"
  if (section == ID_KEDOSHIM):
    return "Kedoshim"
  if (section == ID_EMOR):
    return "Emor"
  if (section == ID_BEHAR):
    return "Behar"
  if (section == ID_BEHUKKOTHAI):
    return "Behukkothai"
  if (section == ID_BEMIDBAR):
    return "Bemidbar"
  if (section == ID_NASO):
    return "Naso"
  if (section == ID_BEHAALOTEHA):
    return "Behaaloteha"
  if (section == ID_SHELAHLEHA):
    return "Shelah Leha"
  if (section == ID_KORAH):
    return "Korah"
  if (section == ID_HUKATH):
    return "Hukath"
  if (section == ID_BALAK):
    return "Balak"
  if (section == ID_PINHAS):
    return "Pinhas"
  if (section == ID_MATOTH):
    return "Matoth"
  if (section == ID_MASEH):
    return "Maseh"
  if (section == ID_DEBARIM):
    return "Debarim, Shabbat Hazon"
  if (section == ID_VAETHANAN):
    return "Vaethanan, Shabbat Nahamu"
  if (section == ID_EKEB):
    return "Ekeb"
  if (section == ID_REEH):
    return "Reeh"
  if (section == ID_SHOFETIM):
    return "Shofetim"
  if (section == ID_KITETSE):
    return "Ki Tetse"
  if (section == ID_KITABO):
    return "Ki Tabo"
  if (section == ID_NITSABIM):
    return "Nitsabim"
  if (section == ID_VAYELEH):
    return "Vayeleh"
  if (section == ID_HAAZINU):
    return "Haazinu"

  #ID_SIMHATHTORAH = 53
  #ID_SIMHATHTORAH_2 = 54
  #ID_SIMHATHTORAH_3 = 55

  if (section == ID_ROSH_HODESH_SHABBAT):
    return "Shabbat Rosh Hodesh"
  if (section == ID_SHEKALIM):
    return "Shabbat Shekalim"
  if (section == ID_ZAHOR):
    return "Shabbat Za'hor"
  if (section == ID_PARAH):
    return "Shabbat Parah"
  if (section == ID_HAHODESH):
    return "Shabbat Hahodesh"
  if (section == ID_HAGGADOL):
    return "Shabbat Hagadol"
  if (section == ID_SHUVA):
    return "Shabbat Shuva"



  if (section == ID_ROSH_HASHANAH_I):
    return "Rosh Hashana I"
  if (section == ID_ROSH_HASHANAH_II):
    return "Rosh Hashana II"
  if (section == ID_FAST_OF_GEDALIAH):
    return "Fast of Gedalia"
  if (section == ID_YOM_KIPPUR):
    return "Yom Kippur"
  ID_SUCCOTH_I = 74
  ID_SUCCOTH_II = 75
  ID_SUCCOTH_III_NO_SHABBAT = 76
  ID_SUCCOTH_III = 77
  ID_SUCCOTH_IV = 78
  ID_SUCCOTH_V_NO_SHABBAT = 79
  ID_SUCCOTH_V = 80
  ID_SUCCOTH_VI_NO_SHABBAT = 81
  ID_SUCCOTH_VI = 82
  ID_HOSHANAH_RABBAH = 83
  ID_HOL_HAMOED_SUCCOTH = 84
  ID_SHEMINI_AZERETH_1 = 85
  ID_FAST_OF_ESTHER = 86
  ID_PURIM = 87
  ID_FAST_OF_TEVET_10 = 88
  ID_PESAH_I = 89
  ID_HOL_HAMOED_PESAH = 90
  ID_PESAH_VII = 91
  ID_PESAH_VIII = 92
  ID_PESAH_VIII_NO_SHABBAT = 93
  ID_SHAVUOTH_I = 94
  ID_SHAVUOTH_II_NO_SHABBAT = 95
  ID_SHAVUOTH_II = 96
  ID_YOM_HAATZMAUT = 97
  ID_FAST_OF_TAMMUZ_17 = 98
  ID_FAST_OF_TISHA_BAV = 99
  ID_CHANUKKAH_I = 100
  ID_CHANUKKAH_II = 101
  ID_CHANUKKAH_III = 102
  ID_CHANUKKAH_IV = 103
  ID_CHANUKKAH_V = 104
  ID_CHANUKKAH_VI = 105
  ID_CHANUKKAH_VI_ROSH_HODESH = 106
  ID_CHANUKKAH_VII = 107
  ID_CHANUKKAH_VII_ROSH_HODESH = 108
  ID_CHANUKKAH_VIII = 109
  ID_SECOND_SHABBAT_CHANUKKAH = 110
  ID_ROSH_HODESH = 111
  ID_PESAH_II = 112
  ID_PESAH_III = 113
  ID_PESAH_IV = 114
  ID_PESAH_IV_NOT_SUNDAY = 115
  ID_PESAH_IV_SUNDAY = 116
  ID_PESAH_V = 117
  ID_PESAH_V_NOT_MONDAY = 118
  ID_PESAH_V_MONDAY = 119
  ID_PESAH_VI = 120

  ID_SPECIAL_1 = 150
  ID_SPECIAL_2 = 151
  ID_SPECIAL_3 = 152
  ID_SPECIAL_4 = 153
  ID_SPECIAL_5 = 154
  ID_SPECIAL_6 = 155
  ID_SPECIAL_7 = 156
  ID_SPECIAL_8 = 157
  ID_SPECIAL_8A = 158
  ID_SPECIAL_9 = 159
  ID_SPECIAL_10 = 161
  ID_SPECIAL_11 = 162
  ID_SPECIAL_12 = 163

  ID_SHEMINI_AZERETH_2 = 170
  ID_SHEMINI_AZERETH_3 = 171
  ID_SHEMINI_AZERETH = 172

  return ""