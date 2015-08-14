#include "viennacl/linalg/inner_prod.hpp"
#include "viennacl/linalg/lu.hpp"
#include "viennacl/tools/timer.hpp"
#include "viennacl/linalg/norm_1.hpp"
#include "viennacl/linalg/norm_2.hpp"
#include "viennacl/linalg/norm_inf.hpp"

#include <iomanip>
#include <stdlib.h>
#include <fstream>
#define FILENAME "file.txt"
template<class T, class F>
void init_random(viennacl::matrix<T, F> & M)
{
    std::vector<T> cM(M.internal_size());
    for (std::size_t i = 0; i < M.size1(); ++i)
        for (std::size_t j = 0; j < M.size2(); ++j)
            cM[F::mem_index(i, j, M.internal_size1(), M.internal_size2())] = T(rand())/T(RAND_MAX);
    viennacl::fast_copy(&cM[0],&cM[0] + cM.size(),M);
}

template<class T>
void init_random(viennacl::vector<T> & x)
{
    std::vector<T> cx(x.internal_size());
    for (std::size_t i = 0; i < cx.size(); ++i)
        cx[i] = T(rand())/T(RAND_MAX);
    viennacl::fast_copy(&cx[0], &cx[0] + cx.size(), x.begin());
}

template<class T>
void bench(size_t BLAS1_N, std::string const & prefix)
{
    std::fstream output;

    using viennacl::linalg::inner_prod;
    using viennacl::linalg::norm_1;
    using viennacl::linalg::norm_2;
    using viennacl::linalg::norm_inf;
    viennacl::tools::timer timer ;
    double time_previous, time_spent;
    size_t Nruns;
    output.open(FILENAME,std::ios::in|std::ios::out|std::ios::ate);
#define BENCHMARK_OP(OPERATION, NAME, PERF, INDEX) \
  if(BLAS1_N==0)\
  {\
    output << std::left << std::setw(8) << prefix + NAME <<",";\
  }\
  else{\
  OPERATION; \
  viennacl::backend::finish();\
  timer.start(); \
  Nruns = 0; \
  time_spent = 0; \
  for(int i=1;i<50;i++) \
  { \
    time_previous = timer.get(); \
    OPERATION; \
    viennacl::backend::finish(); \
    time_spent += timer.get() - time_previous; \
    Nruns+=1; \
  } \
  time_spent/=(double)Nruns; \
  output << std::left << std::setw(8) << PERF<<" " ; \
  }\

    //BLAS1
    {
        viennacl::scalar<T> s(0);
        T alpha = (T)2.4;

        viennacl::vector<T> x(BLAS1_N);
        viennacl::vector<T> y(BLAS1_N);
        viennacl::vector<T> z(BLAS1_N);

        init_random(x);
        init_random(y);
        init_random(z);


        BENCHMARK_OP(swap(x,y),            "swap", std::setprecision(3) << double(4*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(y *= alpha,           "y*=a", std::setprecision(3) << double(2*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(y = x,                "y=x", std::setprecision(3) << double(2*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(y += alpha * x,       "y+=a*x", std::setprecision(3) << double(3*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(y -= alpha * x,       "y-=a*x", std::setprecision(3) << double(3*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(s=inner_prod(x,y),    "dot", std::setprecision(3) << double(2*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(alpha = norm_1(x),    "L1", std::setprecision(3) << double(1*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(alpha = norm_2(x),    "L2", std::setprecision(3) << double(1*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(alpha = norm_inf(x),  "Linf", std::setprecision(3) << double(1*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")

        output.close();
    }
}
int main(int argc, char *argv[])
{
    //fprintf(stdout,"Benchmark : BLAS1_von Franz\n");
    std::fstream output;
    std::size_t BLAS1_N = atoi(argv[1]);
    if(BLAS1_N==0)
    {
        output.open(FILENAME,std::ios::out);
        output << std::left << std::setw(8) << "N" <<",";\
        output.close();
    }

    output.open(FILENAME,std::ios::in|std::ios::out|std::ios::ate);

    if(BLAS1_N!=0) output<< std::setprecision(3) << std::left << std::setw(8) << double(BLAS1_N) <<" ";
    output.close();
    bench<float>(BLAS1_N, "s.");
    bench<double>(BLAS1_N, "d.");
    output.open(FILENAME,std::ios::in|std::ios::out|std::ios::ate);
    output << std::endl;
    output.close();

}








