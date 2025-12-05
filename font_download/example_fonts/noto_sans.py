from font_download.fonts import FontSource, combine_fonts

_COLOR_EMOJI_NOTO_SANS = [
    FontSource(
        # ofl/notocoloremoji/NotoColorEmoji-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notocoloremoji/NotoColorEmoji-Regular.ttf",
    ),
]

_BW_EMOJI_NOTO_SANS = [
    FontSource(
        # ofl/notoemoji/NotoEmoji[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notoemoji/NotoEmoji%5Bwght%5D.ttf"
    )
]

_SYMBOLS_NOTO_SANS = [
    FontSource(
        # ofl/notosansmath/NotoSansMath-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmath/NotoSansMath-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanssymbols/NotoSansSymbols[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssymbols/NotoSansSymbols%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanssymbols2/NotoSansSymbols2-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssymbols2/NotoSansSymbols2-Regular.ttf",
    ),
    FontSource(
        # ofl/notomusic/NotoMusic-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notomusic/NotoMusic-Regular.ttf",
    ),
]

# Generally not necessary, since SignWriting is rendered using an external library
_SIGNWRITING_NOTO_SANS = [
    FontSource(
        # ofl/notosanssignwriting/NotoSansSignWriting-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssignwriting/NotoSansSignWriting-Regular.ttf",
    ),
]

_COMMON_NOTO_SANS = [
    FontSource(
        # ofl/notosans/NotoSans[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosans/NotoSans%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansarabic/NotoSansArabic[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansarabic/NotoSansArabic%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansdevanagari/NotoSansDevanagari[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansdevanagari/NotoSansDevanagari%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansjp/NotoSansJP[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanskr/NotoSansKR[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanssc/NotoSansSC[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanstc/NotoSansTC[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanstc/NotoSansTC%5Bwght%5D.ttf",
    ),
]

_LESS_COMMON_NOTO_SANS = [
    FontSource(
        # ofl/notosansarmenian/NotoSansArmenian[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansarmenian/NotoSansArmenian%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansbengali/NotoSansBengali[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansbengali/NotoSansBengali%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansethiopic/NotoSansEthiopic[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansethiopic/NotoSansEthiopic%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansgeorgian/NotoSansGeorgian[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansgeorgian/NotoSansGeorgian%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansgujarati/NotoSansGujarati[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansgujarati/NotoSansGujarati%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansgurmukhi/NotoSansGurmukhi[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansgurmukhi/NotoSansGurmukhi%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanshebrew/NotoSansHebrew[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanshebrew/NotoSansHebrew%5Bwdth,wght%5D.ttf"
    ),
    FontSource(
        # ofl/notosanshk/NotoSansHK[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanshk/NotoSansHK%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanskannada/NotoSansKannada[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanskannada/NotoSansKannada%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanskhmer/NotoSansKhmer[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanskhmer/NotoSansKhmer%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanslao/NotoSansLao[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanslao/NotoSansLao%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansmalayalam/NotoSansMalayalam[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmalayalam/NotoSansMalayalam%5Bwdth,wght%5D.ttf"
    ),
    FontSource(
        # ofl/notosansmongolian/NotoSansMongolian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmongolian/NotoSansMongolian-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansmyanmar/NotoSansMyanmar[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmyanmar/NotoSansMyanmar%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansoriya/NotoSansOriya[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansoriya/NotoSansOriya%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanssinhala/NotoSansSinhala[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssinhala/NotoSansSinhala%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanssyriac/NotoSansSyriac[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssyriac/NotoSansSyriac%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanstamil/NotoSansTamil[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanstamil/NotoSansTamil%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanstamilsupplement/NotoSansTamilSupplement-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanstamilsupplement/NotoSansTamilSupplement-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanstelugu/NotoSansTelugu[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanstelugu/NotoSansTelugu%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansthai/NotoSansThai[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansthai/NotoSansThai%5Bwdth,wght%5D.ttf",
    ),
]

_RARE_NOTO_SANS = [
    FontSource(
        # ofl/notosansadlam/NotoSansAdlam[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansadlam/NotoSansAdlam%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansanatolianhieroglyphs/NotoSansAnatolianHieroglyphs-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansanatolianhieroglyphs/NotoSansAnatolianHieroglyphs-Regular.ttf"
    ),
    FontSource(
        # ofl/notosansavestan/NotoSansAvestan-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansavestan/NotoSansAvestan-Regular.ttf"
    ),
    FontSource(
        # ofl/notosansbalinese/NotoSansBalinese[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansbalinese/NotoSansBalinese%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansbamum/NotoSansBamum[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansbamum/NotoSansBamum%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansbassavah/NotoSansBassaVah[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansbassavah/NotoSansBassaVah%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansbatak/NotoSansBatak-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansbatak/NotoSansBatak-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansbhaiksuki/NotoSansBhaiksuki-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansbhaiksuki/NotoSansBhaiksuki-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansbrahmi/NotoSansBrahmi-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansbrahmi/NotoSansBrahmi-Regular.ttf"
    ),
    FontSource(
        # ofl/notosansbuginese/NotoSansBuginese-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansbuginese/NotoSansBuginese-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansbuhid/NotoSansBuhid-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansbuhid/NotoSansBuhid-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanscanadianaboriginal/NotoSansCanadianAboriginal[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanscanadianaboriginal/NotoSansCanadianAboriginal%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanscarian/NotoSansCarian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanscarian/NotoSansCarian-Regular.ttf"
    ),
    FontSource(
        # ofl/notosanscaucasianalbanian/NotoSansCaucasianAlbanian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanscaucasianalbanian/NotoSansCaucasianAlbanian-Regular.ttf"
    ),
    FontSource(
        # ofl/notosanschakma/NotoSansChakma-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanschakma/NotoSansChakma-Regular.ttf"
    ),
    FontSource(
        # ofl/notosanscham/NotoSansCham[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanscham/NotoSansCham%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanscherokee/NotoSansCherokee[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanscherokee/NotoSansCherokee%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanschorasmian/NotoSansChorasmian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanschorasmian/NotoSansChorasmian-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanscoptic/NotoSansCoptic-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanscoptic/NotoSansCoptic-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanscuneiform/NotoSansCuneiform-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanscuneiform/NotoSansCuneiform-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanscypriot/NotoSansCypriot-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanscypriot/NotoSansCypriot-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanscyprominoan/NotoSansCyproMinoan-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanscyprominoan/NotoSansCyproMinoan-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansdeseret/NotoSansDeseret-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansdeseret/NotoSansDeseret-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansduployan/NotoSansDuployan-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansduployan/NotoSansDuployan-Regular.ttf"
    ),
    FontSource(
        # ofl/notosansegyptianhieroglyphs/NotoSansEgyptianHieroglyphs-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansegyptianhieroglyphs/NotoSansEgyptianHieroglyphs-Regular.ttf"
    ),
    FontSource(
        # ofl/notosanselbasan/NotoSansElbasan-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanselbasan/NotoSansElbasan-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanselymaic/NotoSansElymaic-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanselymaic/NotoSansElymaic-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansglagolitic/NotoSansGlagolitic-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansglagolitic/NotoSansGlagolitic-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansgothic/NotoSansGothic-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansgothic/NotoSansGothic-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansgrantha/NotoSansGrantha-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansgrantha/NotoSansGrantha-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansgunjalagondi/NotoSansGunjalaGondi[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansgunjalagondi/NotoSansGunjalaGondi%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanshanifirohingya/NotoSansHanifiRohingya[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanshanifirohingya/NotoSansHanifiRohingya%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanshanunoo/NotoSansHanunoo-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanshanunoo/NotoSansHanunoo-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanshatran/NotoSansHatran-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanshatran/NotoSansHatran-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansimperialaramaic/NotoSansImperialAramaic-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansimperialaramaic/NotoSansImperialAramaic-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansindicsiyaqnumbers/NotoSansIndicSiyaqNumbers-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansindicsiyaqnumbers/NotoSansIndicSiyaqNumbers-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansinscriptionalpahlavi/NotoSansInscriptionalPahlavi-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansinscriptionalpahlavi/NotoSansInscriptionalPahlavi-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansinscriptionalparthian/NotoSansInscriptionalParthian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansinscriptionalparthian/NotoSansInscriptionalParthian-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansjavanese/NotoSansJavanese[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansjavanese/NotoSansJavanese%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanskaithi/NotoSansKaithi-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanskaithi/NotoSansKaithi-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanskawi/NotoSansKawi[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanskawi/NotoSansKawi%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanskayahli/NotoSansKayahLi[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanskayahli/NotoSansKayahLi%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanskharoshthi/NotoSansKharoshthi-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanskharoshthi/NotoSansKharoshthi-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanskhojki/NotoSansKhojki-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanskhojki/NotoSansKhojki-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanskhudawadi/NotoSansKhudawadi-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanskhudawadi/NotoSansKhudawadi-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanslepcha/NotoSansLepcha-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanslepcha/NotoSansLepcha-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanslimbu/NotoSansLimbu-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanslimbu/NotoSansLimbu-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanslineara/NotoSansLinearA-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanslineara/NotoSansLinearA-Regular.ttf"
    ),
    FontSource(
        # ofl/notosanslinearb/NotoSansLinearB-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanslinearb/NotoSansLinearB-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanslisu/NotoSansLisu[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanslisu/NotoSansLisu%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanslycian/NotoSansLycian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanslycian/NotoSansLycian-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanslydian/NotoSansLydian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanslydian/NotoSansLydian-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansmahajani/NotoSansMahajani-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmahajani/NotoSansMahajani-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansmandaic/NotoSansMandaic-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmandaic/NotoSansMandaic-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansmanichaean/NotoSansManichaean-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmanichaean/NotoSansManichaean-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansmarchen/NotoSansMarchen-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmarchen/NotoSansMarchen-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansmasaramgondi/NotoSansMasaramGondi-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmasaramgondi/NotoSansMasaramGondi-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansmayannumerals/NotoSansMayanNumerals-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmayannumerals/NotoSansMayanNumerals-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansmedefaidrin/NotoSansMedefaidrin[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmedefaidrin/NotoSansMedefaidrin%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansmeeteimayek/NotoSansMeeteiMayek[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmeeteimayek/NotoSansMeeteiMayek%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansmendekikakui/NotoSansMendeKikakui-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmendekikakui/NotoSansMendeKikakui-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansmeroitic/NotoSansMeroitic-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmeroitic/NotoSansMeroitic-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansmiao/NotoSansMiao-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmiao/NotoSansMiao-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansmodi/NotoSansModi-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmodi/NotoSansModi-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansmro/NotoSansMro-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmro/NotoSansMro-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansmultani/NotoSansMultani-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmultani/NotoSansMultani-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansnabataean/NotoSansNabataean-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansnabataean/NotoSansNabataean-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansnagmundari/NotoSansNagMundari[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansnagmundari/NotoSansNagMundari%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansnandinagari/NotoSansNandinagari-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansnandinagari/NotoSansNandinagari-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansnewa/NotoSansNewa-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansnewa/NotoSansNewa-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansnewtailue/NotoSansNewTaiLue[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansnewtailue/NotoSansNewTaiLue%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansnko/NotoSansNKo-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansnko/NotoSansNKo-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansnushu/NotoSansNushu-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansnushu/NotoSansNushu-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansogham/NotoSansOgham-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansogham/NotoSansOgham-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansolchiki/NotoSansOlChiki[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansolchiki/NotoSansOlChiki%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansoldhungarian/NotoSansOldHungarian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansoldhungarian/NotoSansOldHungarian-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansolditalic/NotoSansOldItalic-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansolditalic/NotoSansOldItalic-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansoldnortharabian/NotoSansOldNorthArabian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansoldnortharabian/NotoSansOldNorthArabian-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansoldpermic/NotoSansOldPermic-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansoldpermic/NotoSansOldPermic-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansoldpersian/NotoSansOldPersian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansoldpersian/NotoSansOldPersian-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansoldsogdian/NotoSansOldSogdian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansoldsogdian/NotoSansOldSogdian-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansoldsoutharabian/NotoSansOldSouthArabian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansoldsoutharabian/NotoSansOldSouthArabian-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansoldturkic/NotoSansOldTurkic-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansoldturkic/NotoSansOldTurkic-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansosage/NotoSansOsage-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansosage/NotoSansOsage-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansosmanya/NotoSansOsmanya-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansosmanya/NotoSansOsmanya-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanspahawhhmong/NotoSansPahawhHmong-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanspahawhhmong/NotoSansPahawhHmong-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanspalmyrene/NotoSansPalmyrene-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanspalmyrene/NotoSansPalmyrene-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanspaucinhau/NotoSansPauCinHau-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanspaucinhau/NotoSansPauCinHau-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansphagspa/NotoSansPhagsPa-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansphagspa/NotoSansPhagsPa-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansphoenician/NotoSansPhoenician-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansphoenician/NotoSansPhoenician-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanspsalterpahlavi/NotoSansPsalterPahlavi-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanspsalterpahlavi/NotoSansPsalterPahlavi-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansrejang/NotoSansRejang-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansrejang/NotoSansRejang-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansrunic/NotoSansRunic-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansrunic/NotoSansRunic-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanssamaritan/NotoSansSamaritan-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssamaritan/NotoSansSamaritan-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanssaurashtra/NotoSansSaurashtra-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssaurashtra/NotoSansSaurashtra-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanssharada/NotoSansSharada-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssharada/NotoSansSharada-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansshavian/NotoSansShavian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansshavian/NotoSansShavian-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanssiddham/NotoSansSiddham-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssiddham/NotoSansSiddham-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanssogdian/NotoSansSogdian-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssogdian/NotoSansSogdian-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanssorasompeng/NotoSansSoraSompeng[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssorasompeng/NotoSansSoraSompeng%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanssoyombo/NotoSansSoyombo-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssoyombo/NotoSansSoyombo-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanssundanese/NotoSansSundanese[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssundanese/NotoSansSundanese%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanssunuwar/NotoSansSunuwar-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssunuwar/NotoSansSunuwar-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanssylotinagri/NotoSansSylotiNagri-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssylotinagri/NotoSansSylotiNagri-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanssyriaceastern/NotoSansSyriacEastern[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanssyriaceastern/NotoSansSyriacEastern%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanstagalog/NotoSansTagalog-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanstagalog/NotoSansTagalog-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanstagbanwa/NotoSansTagbanwa-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanstagbanwa/NotoSansTagbanwa-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanstaile/NotoSansTaiLe-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanstaile/NotoSansTaiLe-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanstaitham/NotoSansTaiTham[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanstaitham/NotoSansTaiTham%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanstaiviet/NotoSansTaiViet-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanstaiviet/NotoSansTaiViet-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanstakri/NotoSansTakri-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanstakri/NotoSansTakri-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanstangsa/NotoSansTangsa[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanstangsa/NotoSansTangsa%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansthaana/NotoSansThaana[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansthaana/NotoSansThaana%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanstifinagh/NotoSansTifinagh-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanstifinagh/NotoSansTifinagh-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanstirhuta/NotoSansTirhuta-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanstirhuta/NotoSansTirhuta-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansugaritic/NotoSansUgaritic-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansugaritic/NotoSansUgaritic-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansvai/NotoSansVai-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansvai/NotoSansVai-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansvithkuqi/NotoSansVithkuqi[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansvithkuqi/NotoSansVithkuqi%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosanswancho/NotoSansWancho-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanswancho/NotoSansWancho-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanswarangciti/NotoSansWarangCiti-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanswarangciti/NotoSansWarangCiti-Regular.ttf",
    ),
    FontSource(
        # ofl/notosansyi/NotoSansYi-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansyi/NotoSansYi-Regular.ttf",
    ),
    FontSource(
        # ofl/notosanszanabazarsquare/NotoSansZanabazarSquare-Regular.ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanszanabazarsquare/NotoSansZanabazarSquare-Regular.ttf",
    ),
]

_OTHER_STYLES_NOTO_SANS = [
    FontSource(
        # ofl/notosans/NotoSans-Italic[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosans/NotoSans-Italic%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansadlamunjoined/NotoSansAdlamUnjoined[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansadlamunjoined/NotoSansAdlamUnjoined%5Bwght%5D.ttf"
    ),
    FontSource(
        # ofl/notosanslaolooped/NotoSansLaoLooped[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosanslaolooped/NotoSansLaoLooped%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansmono/NotoSansMono[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansmono/NotoSansMono%5Bwdth,wght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansnkounjoined/NotoSansNKoUnjoined[wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansnkounjoined/NotoSansNKoUnjoined%5Bwght%5D.ttf",
    ),
    FontSource(
        # ofl/notosansthailooped/NotoSansThaiLooped[wdth,wght].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansthailooped/NotoSansThaiLooped%5Bwdth,wght%5D.ttf",
    ),
]

FONTS_NOTO_SANS = combine_fonts(
    _COMMON_NOTO_SANS,
    _LESS_COMMON_NOTO_SANS,
    _RARE_NOTO_SANS,
    _COLOR_EMOJI_NOTO_SANS,
    _SYMBOLS_NOTO_SANS,
)

FONTS_NOTO_SANS_BW = combine_fonts(
    _COMMON_NOTO_SANS,
    _LESS_COMMON_NOTO_SANS,
    _RARE_NOTO_SANS,
    _BW_EMOJI_NOTO_SANS,
    _SYMBOLS_NOTO_SANS,
)

FONTS_NOTO_SANS_MINIMAL = combine_fonts(
    _COMMON_NOTO_SANS,
)
