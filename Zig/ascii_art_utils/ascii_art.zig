const std = @import("std");

/// ASCII Art font definitions
pub const Font = enum {
    standard,
    banner,
    mini,
    slant,
    
    /// Returns the font data for the selected font
    pub fn getData(self: Font) []const u8 {
        return switch (self) {
            .standard => standard_font,
            .banner => banner_font,
            .mini => mini_font,
            .slant => slant_font,
        };
    }
    
    /// Returns the height of the font in lines
    pub fn getHeight(self: Font) usize {
        return switch (self) {
            .standard, .slant => 6,
            .banner => 5,
            .mini => 3,
        };
    }
    
    /// Returns the width of each character in the font
    pub fn getCharWidth(self: Font) usize {
        return switch (self) {
            .standard, .slant => 6,
            .banner => 5,
            .mini => 3,
        };
    }
};

/// Standard ASCII font (6 lines height, 6 chars width per character)
const standard_font: []const u8 = 
    "      \n      \n      \n      \n      \n      " ++ // space
    "  !!  \n  !!  \n  !!  \n  !!  \n      \n  !!  " ++ // !
    " !! !!\n !! !!\n      \n      \n      \n      " ++ // "
    " #### \n##  ##\n######\n##  ##\n######\n##  ##" ++ // #
    "  ### \n## #  \n #####\n  # ##\n  ### \n  #   " ++ // $
    "##   #\n#  #  \n   #  \n  #   \n #  # \n#   ##" ++ // %
    " ###  \n#   # \n# ##  \n ### #\n#   # \n #####" ++ // &
    "  ##  \n  ##  \n      \n      \n      \n      " ++ // '
    "  ##  \n #    \n#     \n#     \n #    \n  ##  " ++ // (
    "  ##  \n    # \n     #\n     #\n    # \n  ##  " ++ // )
    "      \n#  # #\n #### \n######\n #### \n#  # #" ++ // *
    "      \n  ##  \n  ##  \n######\n  ##  \n  ##  " ++ // +
    "      \n      \n      \n      \n  ##  \n #    " ++ // ,
    "      \n      \n      \n######\n      \n      " ++ // -
    "      \n      \n      \n      \n  ##  \n      " ++ // .
    "     #\n    # \n   #  \n  #   \n #    \n#     " ++ // /
    " ###  \n#   ##\n#  # #\n# #  #\n##   #\n ###  " ++ // 0
    "  ##  \n ###  \n  ##  \n  ##  \n  ##  \n##### " ++ // 1
    " ###  \n#   # \n    # \n  ##  \n #    \n##### " ++ // 2
    " #### \n     #\n  ### \n     #\n     #\n #### " ++ // 3
    "#   # \n#   # \n#   # \n##### \n    # \n    # " ++ // 4
    "##### \n#     \n####  \n     #\n#    #\n #### " ++ // 5
    "  ### \n #    \n#     \n##### \n#    #\n #### " ++ // 6
    "##### \n    # \n   #  \n  #   \n #    \n#     " ++ // 7
    " ###  \n#   # \n # #  \n#   # \n#   # \n ###  " ++ // 8
    " #### \n#    #\n #####\n     #\n    # \n ###  " ++ // 9
    "      \n  ##  \n      \n      \n  ##  \n      " ++ // :
    "      \n  ##  \n      \n      \n  ##  \n #    " ++ // ;
    "   #  \n  #   \n #    \n #    \n  #   \n   #  " ++ // <
    "      \n      \n######\n      \n######\n      " ++ // =
    "  #   \n   #  \n    # \n    # \n   #  \n  #   " ++ // >
    " ###  \n#   # \n   #  \n  #   \n      \n  #   " ++ // ?
    " #### \n#    #\n# ## #\n# # # #\n# ### \n #####" ++ // @
    "  ##  \n #  # \n#    #\n######\n#    #\n#    #" ++ // A
    "##### \n#    #\n##### \n#    #\n#    #\n##### " ++ // B
    " #### \n#     \n#     \n#     \n#     \n #### " ++ // C
    "##### \n#    #\n#    #\n#    #\n#    #\n##### " ++ // D
    "######\n#     \n####  \n#     \n#     \n######" ++ // E
    "######\n#     \n####  \n#     \n#     \n#     " ++ // F
    " #### \n#     \n#  ###\n#    #\n#    #\n #####" ++ // G
    "#    #\n#    #\n######\n#    #\n#    #\n#    #" ++ // H
    "##### \n  ##  \n  ##  \n  ##  \n  ##  \n##### " ++ // I
    "######\n    # \n    # \n#   # \n#   # \n ###  " ++ // J
    "#    #\n#   # \n####  \n#   # \n#    #\n#    #" ++ // K
    "#     \n#     \n#     \n#     \n#     \n######" ++ // L
    "#    #\n##  ##\n# ## #\n#    #\n#    #\n#    #" ++ // M
    "#    #\n##   #\n# #  #\n#  # #\n#   ##\n#    #" ++ // N
    " #### \n#    #\n#    #\n#    #\n#    #\n #### " ++ // O
    "##### \n#    #\n##### \n#     \n#     \n#     " ++ // P
    " #### \n#    #\n#    #\n#  # #\n#   # \n ### #" ++ // Q
    "##### \n#    #\n##### \n#  #  \n#   # \n#    #" ++ // R
    " #####\n#     \n #### \n     #\n     #\n##### " ++ // S
    "######\n  ##  \n  ##  \n  ##  \n  ##  \n  ##  " ++ // T
    "#    #\n#    #\n#    #\n#    #\n#    #\n #### " ++ // U
    "#    #\n#    #\n#    #\n #  # \n #  # \n  ##  " ++ // V
    "#    #\n#    #\n#    #\n# ## #\n##  ##\n#    #" ++ // W
    "#    #\n #  # \n  ##  \n  ##  \n #  # \n#    #" ++ // X
    "#    #\n #  # \n  ##  \n  ##  \n  ##  \n  ##  " ++ // Y
    "######\n    # \n   #  \n  #   \n #    \n######" ++ // Z
    " #### \n #    \n #    \n #    \n #    \n #### " ++ // [
    "#     \n #    \n  #   \n   #  \n    # \n     #" ++ // \
    " #### \n    # \n    # \n    # \n    # \n #### " ++ // ]
    "  ##  \n #  # \n#    #\n      \n      \n      " ++ // ^
    "      \n      \n      \n      \n      \n######" ++ // _
    " ##   \n  #   \n      \n      \n      \n      " ++ // `
    "      \n      \n #### \n    # \n #  # \n #### " ++ // a
    "#     \n#     \n##### \n#    #\n#    #\n##### " ++ // b
    "      \n      \n #### \n#     \n#     \n #### " ++ // c
    "    # \n    # \n #####\n#    #\n#    #\n #####" ++ // d
    "      \n      \n #### \n##### \n#     \n #### " ++ // e
    "  ##  \n #  # \n #    \n####  \n #    \n #    " ++ // f
    "      \n      \n #####\n#    #\n #####\n    # \n #### " ++ // g
    "#     \n#     \n##### \n#    #\n#    #\n#    #" ++ // h
    "  #   \n      \n ##   \n  #   \n  #   \n ###  " ++ // i
    "   #  \n      \n  ##  \n   #  \n#  #  \n ##   " ++ // j
    "#     \n#     \n#  #  \n###   \n#  #  \n#   # " ++ // k
    " ##   \n  #   \n  #   \n  #   \n  #   \n ###  " ++ // l
    "      \n      \n### # \n# # # \n# # # \n#   # " ++ // m
    "      \n      \n##### \n#    #\n#    #\n#    #" ++ // n
    "      \n      \n #### \n#    #\n#    #\n #### " ++ // o
    "      \n      \n##### \n#    #\n##### \n#     " ++ // p
    "      \n      \n #####\n#    #\n #####\n    # " ++ // q
    "      \n      \n# ### \n##    \n#     \n#     " ++ // r
    "      \n      \n #####\n#     \n     #\n##### " ++ // s
    " #    \n #    \n####  \n #    \n #  # \n  ##  " ++ // t
    "      \n      \n#    #\n#    #\n#    #\n #####" ++ // u
    "      \n      \n#    #\n#    #\n #  # \n  ##  " ++ // v
    "      \n      \n#    #\n# ## #\n##  ##\n#    #" ++ // w
    "      \n      \n#    #\n #### \n#    #\n#    #" ++ // x
    "      \n      \n#    #\n #  # \n  ##  \n  #   \n ##   " ++ // y
    "      \n      \n######\n   #  \n  #   \n######" ++ // z
    "  ### \n #    \n #    \n##    \n #    \n  ### " ++ // {
    "  ##  \n  ##  \n  ##  \n  ##  \n  ##  \n  ##  " ++ // |
    "###   \n    # \n    # \n    ##\n    # \n###   " ++ // }
    "  #  #\n # #  \n      \n      \n      \n      ";  // ~

/// Banner font (5 lines height, 5 chars width)
const banner_font: []const u8 = 
    "    \n    \n    \n    \n    " ++ // space
    " ## \n ## \n ## \n    \n ## " ++ // !
    "## ##\n## ##\n     \n     \n     " ++ // "
    " # # \n#####\n # # \n#####\n # # " ++ // #
    " ### \n# #  \n ### \n  # #\n ### " ++ // $
    "#  # \n#  # \n  #  \n #  #\n#  # " ++ // %
    " ##  \n#  # \n ### \n# #  \n # ##" ++ // &
    " ##\n # \n   \n   \n   " ++ // '
    "  # \n #  \n#   \n #  \n  # " ++ // (
    "#   \n #  \n  # \n #  \n#   " ++ // )
    "     \n# # #\n ### \n# # #\n     " ++ // *
    "     \n  #  \n ### \n  #  \n     " ++ // +
    "    \n    \n    \n ## \n #  " ++ // ,
    "    \n    \n ###\n    \n    " ++ // -
    "    \n    \n    \n    \n ## " ++ // .
    "   #\n  # \n #  \n#   \n    " ++ // /
    " ### \n#   #\n# # #\n#   #\n ### " ++ // 0
    "  #  \n ##  \n  #  \n  #  \n ### " ++ // 1
    " ### \n    #\n ### \n#    \n#####" ++ // 2
    " ### \n    #\n ### \n    #\n ### " ++ // 3
    "#   #\n#   #\n#####\n    #\n    #" ++ // 4
    "#####\n#    \n#### \n    #\n#### " ++ // 5
    " ### \n#    \n#### \n#   #\n ### " ++ // 6
    "#####\n    #\n   # \n  #  \n  #  " ++ // 7
    " ### \n#   #\n ### \n#   #\n ### " ++ // 8
    " ### \n#   #\n ####\n    #\n ### " ++ // 9
    "    \n ## \n    \n ## \n    " ++ // :
    "    \n ## \n    \n ## \n #  " ++ // ;
    "  # \n #  \n#   \n #  \n  # " ++ // <
    "    \n####\n    \n####\n    " ++ // =
    "#   \n #  \n  # \n #  \n#   " ++ // >
    " ### \n#   #\n  ## \n     \n  #  " ++ // ?
    " ### \n# # #\n# # #\n# ## \n ### " ++ // @
    " ### \n#   #\n#####\n#   #\n#   #" ++ // A
    "#### \n#   #\n#### \n#   #\n#### " ++ // B
    " ### \n#    \n#    \n#    \n ### " ++ // C
    "#### \n#   #\n#   #\n#   #\n#### " ++ // D
    "#####\n#    \n#### \n#    \n#####" ++ // E
    "#####\n#    \n#### \n#    \n#    " ++ // F
    " ### \n#    \n# ###\n#   #\n ### " ++ // G
    "#   #\n#   #\n#####\n#   #\n#   #" ++ // H
    " ### \n  #  \n  #  \n  #  \n ### " ++ // I
    "  ###\n   # \n   # \n#  # \n ##  " ++ // J
    "#   #\n#  # \n###  \n#  # \n#   #" ++ // K
    "#    \n#    \n#    \n#    \n#####" ++ // L
    "#   #\n## ##\n# # #\n#   #\n#   #" ++ // M
    "#   #\n##  #\n# # #\n#  ##\n#   #" ++ // N
    " ### \n#   #\n#   #\n#   #\n ### " ++ // O
    "#### \n#   #\n#### \n#    \n#    " ++ // P
    " ### \n#   #\n# # #\n#  # \n ## #" ++ // Q
    "#### \n#   #\n#### \n#  # \n#   #" ++ // R
    " ####\n#    \n ### \n    #\n#### " ++ // S
    "#####\n  #  \n  #  \n  #  \n  #  " ++ // T
    "#   #\n#   #\n#   #\n#   #\n ### " ++ // U
    "#   #\n#   #\n#   #\n # # \n  #  " ++ // V
    "#   #\n#   #\n# # #\n## ##\n#   #" ++ // W
    "#   #\n # # \n  #  \n # # \n#   #" ++ // X
    "#   #\n # # \n  #  \n  #  \n  #  " ++ // Y
    "#####\n   # \n  #  \n #   \n#####" ++ // Z
    " ### \n #   \n #   \n #   \n ### " ++ // [
    "#   \n #  \n  # \n   #\n    " ++ // \
    " ### \n   # \n   # \n   # \n ### " ++ // ]
    "  #  \n # # \n#   #\n     \n     " ++ // ^
    "     \n     \n     \n     \n#####" ++ // _
    " #  \n  # \n    \n    \n    " ++ // `
    "     \n     \n ### \n#  # \n ####" ++ // a
    "#    \n#    \n#### \n#   #\n#### " ++ // b
    "     \n     \n ### \n#    \n ### " ++ // c
    "    #\n    #\n ####\n#   #\n ####" ++ // d
    "     \n     \n ### \n### #\n ####" ++ // e
    " ## \n #  \n### \n #  \n #  " ++ // f
    "     \n     \n ####\n#  # \n ####\n    #\n ### " ++ // g
    "#    \n#    \n#### \n#   #\n#   #" ++ // h
    " # \n   \n## \n # \n###" ++ // i
    "  # \n    \n ## \n  # \n# # \n ##  " ++ // j
    "#   \n# # \n##  \n# # \n#  #" ++ // k
    "## \n # \n # \n # \n###" ++ // l
    "     \n     \n### #\n# # #\n# # #" ++ // m
    "     \n     \n#### \n#   #\n#   #" ++ // n
    "     \n     \n ### \n#   #\n ### " ++ // o
    "     \n     \n#### \n#   #\n#### \n#    " ++ // p
    "     \n     \n ####\n#   #\n ####\n    #" ++ // q
    "    \n    \n### \n#   \n#   " ++ // r
    "    \n    \n ###\n#   \n ###" ++ // s
    "#   \n##  \n#   \n#   \n ## " ++ // t
    "     \n     \n#   #\n#   #\n ####" ++ // u
    "    \n    \n#  #\n#  #\n ## " ++ // v
    "     \n     \n#   #\n# # #\n# # #" ++ // w
    "    \n    \n#  #\n ## \n#  #" ++ // x
    "    \n    \n#  #\n ## \n #  \n##  " ++ // y
    "    \n    \n####\n  # \n####" ++ // z
    "  ##\n #  \n##  \n #  \n  ##" ++ // {
    " # \n # \n # \n # \n # " ++ // |
    "##  \n  # \n  ##\n  # \n##  " ++ // }
    "     \n ## #\n# ## \n     \n     ";  // ~

/// Mini font (3 lines height, 3 chars width)
const mini_font: []const u8 = 
    "   \n   \n   " ++ // space
    " # \n # \n   " ++ // !
    "# #\n   \n   " ++ // "
    "# #\n###\n# #" ++ // #
    " # \n## \n # " ++ // $
    "#  \n  #\n#  " ++ // %
    " # \n# #\n ##" ++ // &
    " # \n   \n   " ++ // '
    " # \n#  \n # " ++ // (
    "#  \n # \n#  " ++ // )
    "# #\n # \n# #" ++ // *
    "   \n # \n###" ++ // +
    "   \n # \n#  " ++ // ,
    "   \n###\n   " ++ // -
    "   \n   \n # " ++ // .
    "  #\n # \n#  " ++ // /
    " # \n# #\n # " ++ // 0
    " # \n## \n # " ++ // 1
    "## \n # \n## " ++ // 2
    "## \n## \n## " ++ // 3
    "# #\n###\n  #" ++ // 4
    "###\n## \n###" ++ // 5
    " # \n## \n###" ++ // 6
    "###\n  #\n  #" ++ // 7
    "###\n###\n###" ++ // 8
    "###\n###\n  #" ++ // 9
    "   \n # \n # " ++ // :
    "   \n # \n#  " ++ // ;
    "  #\n # \n#  " ++ // <
    "   \n###\n###" ++ // =
    "#  \n # \n  #" ++ // >
    "## \n # \n   " ++ // ?
    "###\n###\n###" ++ // @
    " # \n# #\n###" ++ // A
    "## \n## \n## " ++ // B
    " # \n#  \n # " ++ // C
    "## \n# #\n## " ++ // D
    "## \n## \n## " ++ // E
    "## \n## \n#  " ++ // F
    " # \n# #\n ##" ++ // G
    "# #\n###\n# #" ++ // H
    " # \n # \n # " ++ // I
    " # \n # \n## " ++ // J
    "# #\n## \n# #" ++ // K
    "#  \n#  \n## " ++ // L
    "# #\n###\n# #" ++ // M
    "# #\n###\n# #" ++ // N
    " # \n# #\n # " ++ // O
    "## \n## \n#  " ++ // P
    " # \n# #\n ##" ++ // Q
    "## \n## \n# #" ++ // R
    "## \n## \n## " ++ // S
    "###\n # \n # " ++ // T
    "# #\n# #\n###" ++ // U
    "# #\n# #\n # " ++ // V
    "# #\n###\n# #" ++ // W
    "# #\n # \n# #" ++ // X
    "# #\n # \n # " ++ // Y
    "## \n # \n## " ++ // Z
    "## \n#  \n## " ++ // [
    "#  \n # \n  #" ++ // \
    "## \n  #\n## " ++ // ]
    " # \n# #\n   " ++ // ^
    "   \n   \n###" ++ // _
    "#  \n   \n   " ++ // `
    "   \n # \n# #" ++ // a
    "#  \n## \n# #" ++ // b
    "   \n ##\n## " ++ // c
    "  #\n ##\n# #" ++ // d
    "   \n###\n## " ++ // e
    " # \n## \n#  " ++ // f
    "   \n###\n ##\n#  " ++ // g
    "#  \n## \n# #" ++ // h
    "   \n## \n # " ++ // i
    "   \n## \n # \n#  " ++ // j
    "#  \n# #\n# #" ++ // k
    "   \n#  \n## " ++ // l
    "   \n###\n# #" ++ // m
    "   \n## \n# #" ++ // n
    "   \n # \n# #" ++ // o
    "   \n## \n# #\n#  " ++ // p
    "   \n ##\n# #\n  #" ++ // q
    "   \n## \n#  " ++ // r
    "   \n## \n## " ++ // s
    "#  \n## \n # " ++ // t
    "   \n# #\n## " ++ // u
    "   \n# #\n # " ++ // v
    "   \n# #\n###" ++ // w
    "   \n# #\n# #" ++ // x
    "   \n# #\n ##\n#  " ++ // y
    "   \n## \n## " ++ // z
    " # \n#  \n # " ++ // {
    " # \n # \n # " ++ // |
    "#  \n # \n#  " ++ // }
    "   \n# #\n   ";  // ~

/// Slant font (6 lines height, italic style)
const slant_font: []const u8 = 
    "      \n      \n      \n      \n      \n      " ++ // space
    "   ## \n   ## \n   ## \n      \n   ## \n      " ++ // !
    "  ## ##\n  ## ##\n      \n      \n      \n      " ++ // "
    "  #### \n ##  ##\n ######\n##  ## \n###### \n##  ## " ++ // #
    "   ### \n  ## # \n ##### \n  # ## \n  ###  \n  #    " ++ // $
    "##   # \n#  #   \n    #  \n   #   \n  #  # \n #   ##" ++ // %
    "  ###  \n #   # \n # ##  \n  ### #\n #   # \n  #####" ++ // &
    "   ##  \n  ##   \n      \n      \n      \n      " ++ // '
    "   ##  \n  #    \n #     \n #     \n  #    \n   ##  " ++ // (
    "  ##   \n    #  \n     # \n     # \n    #  \n  ##   " ++ // )
    "       \n#  #  #\n ####  \n ######\n  #### \n#  #  #" ++ // *
    "       \n   ##  \n   ##  \n###### \n   ##  \n   ##  " ++ // +
    "       \n       \n       \n       \n   ##  \n  #    " ++ // ,
    "       \n       \n       \n###### \n       \n       " ++ // -
    "       \n       \n       \n       \n   ##  \n       " ++ // .
    "     # \n    #  \n   #   \n  #    \n #     \n#      " ++ // /
    "  ###  \n #   ##\n #  # #\n # #  #\n ##   #\n  ###  " ++ // 0
    "   ##  \n  ###  \n   ##  \n   ##  \n   ##  \n ##### " ++ // 1
    "  ###  \n #   # \n     # \n   ##  \n  #    \n ##### " ++ // 2
    "  #### \n      #\n   ### \n      #\n      #\n  #### " ++ // 3
    "#   #  \n#   #  \n#   #  \n#####  \n    #  \n    #  " ++ // 4
    "#####  \n#      \n####   \n     # \n#    # \n ####  " ++ // 5
    "  ###  \n #     \n#      \n#####  \n#    # \n ####  " ++ // 6
    "#####  \n    #  \n   #   \n  #    \n #     \n#      " ++ // 7
    "  ###  \n #   # \n  # #  \n #   # \n #   # \n  ###  " ++ // 8
    "  #### \n #    #\n  #####\n      #\n     # \n  ###  " ++ // 9
    "       \n   ##  \n       \n       \n   ##  \n       " ++ // :
    "       \n   ##  \n       \n       \n   ##  \n  #    " ++ // ;
    "    #  \n   #   \n  #    \n  #    \n   #   \n    #  " ++ // <
    "       \n       \n###### \n       \n###### \n       " ++ // =
    "  #    \n   #   \n    #  \n    #  \n   #   \n  #    " ++ // >
    "  ###  \n #   # \n    #  \n   #   \n       \n   #   " ++ // ?
    "  #### \n #    #\n # ## #\n # # # #\n # ### \n  #####" ++ // @
    "   ##  \n  #  # \n #    #\n ######\n#    # \n#    # " ++ // A
    "#####  \n#    # \n#####  \n#    # \n#    # \n#####  " ++ // B
    "  #### \n #     \n#      \n#      \n #     \n  #### " ++ // C
    "#####  \n#    # \n#    # \n#    # \n#    # \n#####  " ++ // D
    "###### \n#      \n####   \n#      \n#      \n###### " ++ // E
    "###### \n#      \n####   \n#      \n#      \n#      " ++ // F
    "  #### \n #     \n#  ### \n#    # \n #   # \n  #### " ++ // G
    "#    # \n#    # \n###### \n#    # \n#    # \n#    # " ++ // H
    "#####  \n  ##   \n  ##   \n  ##   \n  ##   \n#####  " ++ // I
    "###### \n     # \n     # \n#    # \n#    # \n ###   " ++ // J
    "#    # \n#   #  \n####   \n#  #   \n#    # \n#    # " ++ // K
    "#      \n#      \n#      \n#      \n#      \n###### " ++ // L
    "#    # \n##  ## \n# ## # \n#    # \n#    # \n#    # " ++ // M
    "#    # \n##   # \n# #  # \n#  # # \n#   ## \n#    # " ++ // N
    "  #### \n #    #\n #    #\n #    #\n #    #\n  #### " ++ // O
    "#####  \n#    # \n#####  \n#      \n#      \n#      " ++ // P
    "  #### \n #    #\n #    #\n #  # #\n #   # \n  ### #" ++ // Q
    "#####  \n#    # \n#####  \n#  #   \n#   #  \n#    # " ++ // R
    "  #####\n #     \n  #### \n     # \n     # \n#####  " ++ // S
    "###### \n  ##   \n  ##   \n  ##   \n  ##   \n  ##   " ++ // T
    "#    # \n#    # \n#    # \n#    # \n#    # \n ####  " ++ // U
    "#    # \n#    # \n#    # \n #  #  \n  # #   \n   #   " ++ // V
    "#    # \n#    # \n#    # \n# ## # \n##  ## \n#    # " ++ // W
    "#    # \n #  #  \n  ##   \n  ##   \n #  #  \n#    # " ++ // X
    "#    # \n #  #  \n  ##   \n  ##   \n  ##   \n  ##   " ++ // Y
    "###### \n     # \n    #  \n   #   \n  #    \n###### " ++ // Z
    "  #### \n  #    \n  #    \n  #    \n  #    \n  #### " ++ // [
    "#      \n #     \n  #    \n   #   \n    #  \n     # " ++ // \
    "  #### \n    #  \n    #  \n    #  \n    #  \n  #### " ++ // ]
    "   ##  \n  #  # \n #    #\n       \n       \n       " ++ // ^
    "       \n       \n       \n       \n       \n###### " ++ // _
    " ##    \n  #    \n       \n       \n       \n       " ++ // `
    "       \n       \n  #### \n     # \n #   # \n  #### " ++ // a
    "#      \n#      \n#####  \n#    # \n#    # \n#####  " ++ // b
    "       \n       \n  #### \n #     \n #     \n  #### " ++ // c
    "     # \n     # \n  #####\n #    #\n #    #\n  #####" ++ // d
    "       \n       \n  #### \n ##### \n #     \n  #### " ++ // e
    "   ##  \n  #  # \n  #    \n ####  \n  #    \n  #    " ++ // f
    "       \n       \n  #####\n #    #\n  #####\n     # \n  ###  " ++ // g
    "#      \n#      \n#####  \n#    # \n#    # \n#    # " ++ // h
    "   #   \n       \n  ##   \n   #   \n   #   \n  ###  " ++ // i
    "    #  \n       \n   ##  \n    #  \n#   #  \n  ##   " ++ // j
    "#      \n#      \n#  #   \n###    \n#  #   \n#   #  " ++ // k
    " ##    \n  #    \n  #    \n  #    \n  #    \n ###   " ++ // l
    "       \n       \n### #  \n# # #  \n# # #  \n#   #  " ++ // m
    "       \n       \n#####  \n#    # \n#    # \n#    # " ++ // n
    "       \n       \n  #### \n #    #\n #    #\n  #### " ++ // o
    "       \n       \n#####  \n#    # \n#####  \n#      " ++ // p
    "       \n       \n  #####\n #    #\n  #####\n     # " ++ // q
    "       \n       \n# ###  \n##     \n#      \n#      " ++ // r
    "       \n       \n  #####\n #     \n     # \n#####  " ++ // s
    "  #    \n  #    \n ####  \n  #    \n  #  # \n   ##  " ++ // t
    "       \n       \n#    # \n#    # \n#    # \n  #####" ++ // u
    "       \n       \n#    # \n #  #  \n  ##   \n   #   \n ##    " ++ // v
    "       \n       \n#    # \n# ## # \n##  ## \n#    # " ++ // w
    "       \n       \n#    # \n  #### \n#    # \n#    # " ++ // x
    "       \n       \n#    # \n #  #  \n  ##   \n  #    \n ##    " ++ // y
    "       \n       \n###### \n    #  \n   #   \n###### " ++ // z
    "   ### \n  #    \n  #    \n ##    \n  #    \n   ### " ++ // {
    "   ##  \n   ##  \n   ##  \n   ##  \n   ##  \n   ##  " ++ // |
    "###    \n    #  \n    #  \n    ## \n    #  \n###    " ++ // }
    "   #  #\n  # #  \n       \n       \n       \n       ";  // ~

/// Character offset table - maps ASCII code to position in font data
const char_offsets: [128]usize = initOffsets();

fn initOffsets() [128]usize {
    var offsets: [128]usize = undefined;
    var offset: usize = 0;
    var char_idx: usize = 32; // Start from space
    
    // Characters in order: space, !, ", #, $, %, &, ', (, ), *, +, ,, -, ., /
    // 0-9, :, ;, <, =, >, ?, @, A-Z, [, \, ], ^, _, `, a-z, {, |, }, ~
    
    // Initialize all to 0
    for (&offsets) |*o| {
        o.* = 0;
    }
    
    // Space (32)
    offsets[32] = 0;
    offset += 37; // 6 lines * 6 chars + 6 newlines = 42 - 5 = 37
    
    // ! to / (33-47)
    char_idx = 33;
    while (char_idx <= 47) : (char_idx += 1) {
        offsets[char_idx] = offset;
        offset += 37;
    }
    
    // 0-9 (48-57)
    char_idx = 48;
    while (char_idx <= 57) : (char_idx += 1) {
        offsets[char_idx] = offset;
        offset += 37;
    }
    
    // : to @ (58-64)
    char_idx = 58;
    while (char_idx <= 64) : (char_idx += 1) {
        offsets[char_idx] = offset;
        offset += 37;
    }
    
    // A-Z (65-90)
    char_idx = 65;
    while (char_idx <= 90) : (char_idx += 1) {
        offsets[char_idx] = offset;
        offset += 37;
    }
    
    // [ to ` (91-96)
    char_idx = 91;
    while (char_idx <= 96) : (char_idx += 1) {
        offsets[char_idx] = offset;
        offset += 37;
    }
    
    // a-z (97-122)
    char_idx = 97;
    while (char_idx <= 122) : (char_idx += 1) {
        offsets[char_idx] = offset;
        offset += 37;
    }
    
    // { to ~ (123-126)
    char_idx = 123;
    while (char_idx <= 126) : (char_idx += 1) {
        offsets[char_idx] = offset;
        offset += 37;
    }
    
    return offsets;
}

/// Get the character art from font data
fn getCharArt(font_data: []const u8, offset: usize, row: usize, char_width: usize) []const u8 {
    // Calculate position: offset + (row * (char_width + 1))
    const row_offset = offset + row * (char_width + 1);
    if (row_offset >= font_data.len) {
        return "";
    }
    
    // Find the end of this row (newline or char_width chars)
    var end = row_offset;
    var count: usize = 0;
    while (end < font_data.len and count < char_width) : (end += 1) {
        if (font_data[end] == '\n') break;
        count += 1;
    }
    
    return font_data[row_offset..end];
}

/// ASCII Art Generator
pub const AsciiArt = struct {
    allocator: std.mem.Allocator,
    font: Font,
    
    const Self = @This();
    
    /// Initialize a new ASCII Art generator
    pub fn init(allocator: std.mem.Allocator, font: Font) Self {
        return .{
            .allocator = allocator,
            .font = font,
        };
    }
    
    /// Generate ASCII art from text
    pub fn generate(self: *Self, text: []const u8) ![]u8 {
        const font_data = self.font.getData();
        const height = self.font.getHeight();
        const char_width = self.font.getCharWidth();
        
        // Split text into lines
        var lines: std.ArrayList([]const u8) = std.ArrayList([]const u8).init(self.allocator);
        defer lines.deinit();
        
        var line_start: usize = 0;
        for (text, 0..) |char, i| {
            if (char == '\n') {
                try lines.append(text[line_start..i]);
                line_start = i + 1;
            }
        }
        if (line_start < text.len) {
            try lines.append(text[line_start..]);
        }
        
        // Calculate total size needed
        var total_size: usize = 0;
        for (lines.items) |line| {
            total_size += line.len * char_width * height + height; // chars + newlines
        }
        total_size += lines.items.len; // line separators
        
        var buffer = try self.allocator.alloc(u8, total_size);
        var pos: usize = 0;
        
        // Generate each line
        for (lines.items) |line| {
            for (0..height) |row| {
                for (line) |char| {
                    if (char >= 32 and char <= 126) {
                        const offset = char_offsets[char];
                        const char_art = getCharArt(font_data, offset, row, char_width);
                        for (char_art) |c| {
                            if (pos < buffer.len) {
                                buffer[pos] = c;
                                pos += 1;
                            }
                        }
                    }
                }
                // Add newline after each row
                if (pos < buffer.len) {
                    buffer[pos] = '\n';
                    pos += 1;
                }
            }
        }
        
        return self.allocator.realloc(buffer, pos);
    }
    
    /// Free resources
    pub fn deinit(self: *Self) void {
        _ = self;
    }
};

/// Generate ASCII art from text (convenience function)
pub fn generateAscii(allocator: std.mem.Allocator, text: []const u8, font: Font) ![]u8 {
    var art = AsciiArt.init(allocator, font);
    return art.generate(text);
}

/// Print ASCII art to stdout
pub fn printAscii(text: []const u8, font: Font) !void {
    const allocator = std.heap.page_allocator;
    var art = AsciiArt.init(allocator, font);
    const output = try art.generate(text);
    defer allocator.free(output);
    
    const stdout = std.io.getStdOut().writer();
    try stdout.print("{s}", .{output});
}

/// Get list of available fonts
pub fn getAvailableFonts() []const []const u8 {
    return &[_][]const u8{
        "standard",
        "banner", 
        "mini",
        "slant",
    };
}

/// Parse font name to Font enum
pub fn parseFontName(name: []const u8) ?Font {
    if (std.mem.eql(u8, name, "standard")) return .standard;
    if (std.mem.eql(u8, name, "banner")) return .banner;
    if (std.mem.eql(u8, name, "mini")) return .mini;
    if (std.mem.eql(u8, name, "slant")) return .slant;
    return null;
}

// ============================================================================
// Tests
// ============================================================================

test "generate basic text" {
    const allocator = std.testing.allocator;
    
    var art = AsciiArt.init(allocator, .standard);
    const result = try art.generate("HI");
    defer allocator.free(result);
    
    try std.testing.expect(result.len > 0);
}

test "generate mini font" {
    const allocator = std.testing.allocator;
    
    var art = AsciiArt.init(allocator, .mini);
    const result = try art.generate("ABC");
    defer allocator.free(result);
    
    try std.testing.expect(result.len > 0);
}

test "generate banner font" {
    const allocator = std.testing.allocator;
    
    var art = AsciiArt.init(allocator, .banner);
    const result = try art.generate("HELLO");
    defer allocator.free(result);
    
    try std.testing.expect(result.len > 0);
}

test "generate slant font" {
    const allocator = std.testing.allocator;
    
    var art = AsciiArt.init(allocator, .slant);
    const result = try art.generate("WORLD");
    defer allocator.free(result);
    
    try std.testing.expect(result.len > 0);
}

test "generate single character" {
    const allocator = std.testing.allocator;
    
    var art = AsciiArt.init(allocator, .standard);
    const result = try art.generate("A");
    defer allocator.free(result);
    
    try std.testing.expect(result.len > 0);
}

test "generate numbers" {
    const allocator = std.testing.allocator;
    
    var art = AsciiArt.init(allocator, .standard);
    const result = try art.generate("123");
    defer allocator.free(result);
    
    try std.testing.expect(result.len > 0);
}

test "generate special characters" {
    const allocator = std.testing.allocator;
    
    var art = AsciiArt.init(allocator, .standard);
    const result = try art.generate("!@#");
    defer allocator.free(result);
    
    try std.testing.expect(result.len > 0);
}

test "generate lowercase" {
    const allocator = std.testing.allocator;
    
    var art = AsciiArt.init(allocator, .standard);
    const result = try art.generate("hello");
    defer allocator.free(result);
    
    try std.testing.expect(result.len > 0);
}

test "generate mixed case" {
    const allocator = std.testing.allocator;
    
    var art = AsciiArt.init(allocator, .standard);
    const result = try art.generate("Hello World");
    defer allocator.free(result);
    
    try std.testing.expect(result.len > 0);
}

test "generate multiline" {
    const allocator = std.testing.allocator;
    
    var art = AsciiArt.init(allocator, .standard);
    const result = try art.generate("AB\nCD");
    defer allocator.free(result);
    
    try std.testing.expect(result.len > 0);
}

test "parse font names" {
    try std.testing.expect(parseFontName("standard") != null);
    try std.testing.expect(parseFontName("banner") != null);
    try std.testing.expect(parseFontName("mini") != null);
    try std.testing.expect(parseFontName("slant") != null);
    try std.testing.expect(parseFontName("unknown") == null);
}

test "available fonts list" {
    const fonts = getAvailableFonts();
    try std.testing.expect(fonts.len == 4);
}

test "convenience function" {
    const allocator = std.testing.allocator;
    const result = try generateAscii(allocator, "TEST", .standard);
    defer allocator.free(result);
    
    try std.testing.expect(result.len > 0);
}

test "font heights" {
    try std.testing.expect(Font.standard.getHeight() == 6);
    try std.testing.expect(Font.banner.getHeight() == 5);
    try std.testing.expect(Font.mini.getHeight() == 3);
    try std.testing.expect(Font.slant.getHeight() == 6);
}