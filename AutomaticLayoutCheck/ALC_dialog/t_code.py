from ALC_dialog.ALC.comparator import ComparatorMeanSquaredError, ComparatorStructuralSimilarityIndex


ref_p = r'C:\Users\Jald\PycharmProjects\AutomaticLayoutCheck\AutomaticLayoutCheck\ALC_dialog\reference_sample.png'
s_p_1 = r'C:\Users\Jald\PycharmProjects\AutomaticLayoutCheck\AutomaticLayoutCheck\ALC_dialog\sample_0.png'
s_p_2 = r'C:\Users\Jald\PycharmProjects\AutomaticLayoutCheck\AutomaticLayoutCheck\ALC_dialog\sample_1.png'
s_p_3 = r'C:\Users\Jald\PycharmProjects\AutomaticLayoutCheck\AutomaticLayoutCheck\ALC_dialog\favicon.ico'

# o = ComparatorMeanSquaredError(ref_p, ref_p).get_similarity_percentages
# x = ComparatorMeanSquaredError(ref_p, s_p_1).get_similarity_percentages
# y = ComparatorMeanSquaredError(ref_p, s_p_2).get_similarity_percentages
# z = ComparatorMeanSquaredError(ref_p, s_p_2).get_similarity_percentages
#
# print(o)
# print(x)
# print(y)
# print(z)


o = ComparatorStructuralSimilarityIndex(ref_p, ref_p).are_images_similar
x = ComparatorStructuralSimilarityIndex(ref_p, s_p_1).are_images_similar
y = ComparatorStructuralSimilarityIndex(ref_p, s_p_2).are_images_similar
z = ComparatorStructuralSimilarityIndex(ref_p, s_p_2).are_images_similar

print(o)
print(x)
print(y)
print(z)



