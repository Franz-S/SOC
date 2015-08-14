#include "viennacl/linalg/norm_1.hpp"
#include "viennacl/linalg/norm_2.hpp"
#include "examples/benchmarks/benchmark-utils.hpp"
#include "viennacl/linalg/inner_prod.hpp"
#include "viennacl/linalg/lu.hpp"
#include "viennacl/linalg/lu.hpp"

#include <iomanip>
#include <stdlib.h>

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
    using viennacl::linalg::inner_prod;
    using viennacl::linalg::prod;
    using viennacl::linalg::lu_factorize;
    using viennacl::trans;

    Timer timer ;
    double time_previous, time_spent;
    size_t Nruns;

#define BENCHMARK_OP(OPERATION, NAME, PERF, INDEX) \
  if(BLAS1_N==0)\
  {\
    std::cout << prefix<<NAME<<",";\
  }\
  else{\
  OPERATION; \
  viennacl::backend::finish();\
  timer.start(); \
  Nruns = 0; \
  time_spent = 0; \
  for(int i=1;i<10;i++) \
  { \
    time_previous = timer.get(); \
    OPERATION; \
    viennacl::backend::finish(); \
    time_spent += timer.get() - time_previous; \
    Nruns+=1; \
  } \
  time_spent/=(double)Nruns; \
  std::cout << std::left << std::setw(8) << PERF<<" " ; \
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


        BENCHMARK_OP(swap(x,y),            "swap", std::setprecision(3) << double(2*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(x *= alpha,           "stretch", std::setprecision(3) << double(2*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(x = y,                "assignment", std::setprecision(3) << double(2*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")

        BENCHMARK_OP(y += alpha * x,       "multiply add", std::setprecision(3) << double(3*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(y -= alpha * x,       "multiply subtract", std::setprecision(3) << double(3*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(s=inner_prod(x,y),    "inner dot product", std::setprecision(3) << double(2*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        /*BENCHMARK_OP(alpha = norm_1(x),    "L1 norm", std::setprecision(3) << double(2*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(alpha = norm_2(x),    "L2 norm", std::setprecision(3) << double(2*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        BENCHMARK_OP(alpha = norm_inf(x),  "Linf norm", std::setprecision(3) << double(2*BLAS1_N*sizeof(T))/time_spent * 1e-9, "GB/s")
        */
    }
}
int main(int argc, char *argv[])
{
    //fprintf(stdout,"Benchmark : BLAS1_von Franz\n");

    std::size_t BLAS1_N = atoi(argv[1]);
    if(BLAS1_N!=0) std::cout << std::setprecision(3) << std::left << std::setw(8) << double(BLAS1_N) <<" ";
    bench<float>(BLAS1_N, "s");
    bench<double>(BLAS1_N, "d");
}

