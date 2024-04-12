
def rotate_90(mat):

    n = len(mat)

    m = len(mat[0])

    new_mat = [[0] * n for _ in range(m)]

    for i in range(n):

        for j in range(m):

            new_mat[j][n - i - 1] = mat[i][j]

    return new_mat

