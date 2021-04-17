 
#include <stdio.h>
#include <math.h>
#include <complex.h>
#include <stdlib.h>

/*
This program calculates Fourier Transform 
using the vector-radix FFT algorithm.
*/

void fft(double complex* x, long int N, int t){
        if(N<=1)return;

        double complex* odd = malloc(N/2 * sizeof(double complex));
        double complex* even = malloc(N/2 * sizeof(double complex));
        for(long int i=0;i<N/2;i++){
                odd[i] = x[2*i+1];
                even[i] = x[2*i];
        }

        fft(even, N/2, t);
        fft(odd, N/2, t);

        for(int i=0;i<N/2;i++){
                               
                double complex w = cexp(2*M_PI*i*I*t/N);                //Twiddle Factor
                x[i] = even[i] + w*odd[i];
                x[i+N/2] = even[i] - w*odd[i];
        }
        free(even);
        free(odd);

        return;
}

void ifft(double complex* x, long int N){

        fft(x, N, -1);

        for(int i=0;i<N;i++)
               x[i] = x[i]/N;

        return;
}

int main(){

        int n = (1<<20);

        double* x = (double*)malloc(n*sizeof(double));


        double complex* X = (double complex*)malloc(n*sizeof(double complex));

        FILE *f, *F;

        f= fopen("x.dat", "r");
        
        int len = 0;
        double a;
        while(!feof(f) && len<n){
            fscanf(f, "%lf", &a);
            X[len] = CMPLX(a,0);
            len++;
    }


        fft(X, n, 1);

        F = fopen("X.dat", "w");
        for(int i=0;i<n;i++)
                fprintf(F, "%1f+%1fi\n", creal(X[i]), cimag(X[i]));



        fclose(f);

        fclose(F);

        return 0;
}
