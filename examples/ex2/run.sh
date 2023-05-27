varwizard --input "static void lsp2poly ( int * var0, const int16_t * var1, int var2 ) { int var3, var4 ; var0 [ 0 ] = 0x400000 ; // 1.0 in (3.22) var0 [ 1 ] = - var1 [ 0 ] << 8 ; // *2 and (0.15) -> (3.22) for ( var3 = 2 ; var3 <= var2 ; var3 ++ ) { var0 [ var3 ] = var0 [ var3 - 2 ] ; for ( var4 = var3 ; var4 > 1 ; var4 -- ) var0 [ var4 ] -= MULL ( var0 [ var4 - 1 ], var1 [ 2 * var3 - 2 ], FRAC_BITS ) - var0 [ var4 - 2 ] ; var0 [ 1 ] -= var1 [ 2 * var3 - 2 ] << 8 ; } }" \
        --lang cpp \
        --model-name codet5-base \
        --output-path out.txt