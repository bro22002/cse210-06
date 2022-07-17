#numero matricola 331968
board = ["#############################",
         "#                           #",
         "# ------------# ------------#",
         "# -### -#### -# -#### -### -#",
         "# +### -#### -# -#### -### +#",
         "# -    -     -  -     -    -#",
         "# --------------------------#",
         "# -### -# -####### -# -### -#",
         "# -    -# -   #    -# -    -#",
         "# ------# ----# ----# ------#",
         "###### -####  #  #### -######",
         "###### -#           # -######",
         "###### -#           # -######",
         "###### -#  #######  # -######",
         "       -   #######    -      ",
         "       -   #######    -      ",
         "###### -#  #######  # -######",
         "###### -#           # -######",
         "###### -#           # -######",
         "###### -#  #######  # -######",
         "#      -      #       -     #",
         "# ------------# ------------#",
         "# -### -#### -# -#### -### -#",
         "# -  # -     -  -     -#   -#",
         "# +--# -------  -------# --+#",
         "### -# -# -####### -# -# -###",
         "#   -  -# -   #    -# -  -  #",
         "# ------# ----# ----# ------#",
         "# -######### -# -######### -#",
         "# -          -  -          -#",
         "# --------------------------#",
         "#############################"]
#create cookies
def cookis ()-> list:
    coordinates_cookis = []

    for riga1 in range(32):
        line = board[riga1]
        for colonna1 in range(29):
            if "-" in line[colonna1]:
                coordinate = (riga1, colonna1) 
                coordinates_cookis.append(coordinate)
        colonna1+=0

    return coordinates_cookis

#create poower ups
def big_cookis () -> list:
    coordinates_cookis = []

    for riga1 in range(32):
        line = board[riga1]
        for colonna1 in range(29):
            if "+" == line[colonna1]:
                coordinate = (riga1, colonna1) 
                coordinates_cookis.append(coordinate)
        colonna1+=0

    return coordinates_cookis
