#include <iostream>
#include <stdlib.h> //rand
#include <time.h> //time
#include <conio.h>
#include <stdio.h>
using namespace std;

/*
TOTAL_LATITUD = 0 == -90 // TOTAL_LATITUD = 180 == 90
TOTAL_LONGITUD = 0 == -180 // TOTAL_LONGITUD = 360 == 180
*/
#define LATITUD 90 //90
#define LONGITUD 180 //180
#define TOTAL_LATITUD 181 //180 = [-90,90] + 1 para incluir al cero
#define TOTAL_LONGITUD 361 //360 = [-180,180] + 1 para incluir al cero

//Definiciones de datos (struct)
struct medida
{
    int segundo;
    int latitud;
    int longitud;
    double temperatura;
};

struct par
{
    int cantidad;
    double promedio;
};

//Operaciones sobre Archivos
//bool LeerEspecial(TipoArchivo archivo, TipoRegistro registro);
//int BuscarBinArchivo(TipoArchivo archivo, Tipo valor);
//void BuscarBinArchivo(TipoArchivo archivo, TipoInfo clave, TipoRegistro Registro);

//Operaciones sobre Arreglos
//void OrdenarArregloPorCampo(TipoArreglo arreglo, int n);
//void CargarSinRepetir(TipoArreglo arreglo, int pos, int n, bool inserto, TipoInfo clave);
//int BuscarBinArreglo(TipoArreglo arreglo, int N, TipoInfo clave);
//void BuscarBinArreglo(TipoArreglo arreglo, int N, TipoInfo clave, int Pos);

//Otras funciones y procedimientos
void CargarDatosPrueba(par matriz[TOTAL_LATITUD][TOTAL_LONGITUD])
{
	for(int j=0; j<50; j++)
	{
		 for (int i = 0; i < 20; i++)
		 {
			  medida m;
			  m.segundo = rand(); //Random
			  m.latitud = -90 + (rand() % TOTAL_LATITUD); //Random en el rango [-90, 90]
			  m.longitud = -180 + (rand() % TOTAL_LONGITUD); //Random en el rango [-180, 180]
			  m.temperatura = (50.f - (-50.f)) * ((double) rand() / (double)RAND_MAX) + (-50.f); //Random en el rango [-50.f, 50.f]

			  int posLatitud = m.latitud + LATITUD; //Relaciono la latitud con el valor correspondiente para la matriz
			  int posLongitud = m.longitud + LONGITUD; //Relaciono la longitud con el valor correspondiente para la matriz

			  int cantidad = matriz[posLatitud][posLongitud].cantidad;
			  float promedio = matriz[posLatitud][posLongitud].promedio;

			  cantidad += 1;
			  promedio = (promedio + m.temperatura) / cantidad;

			  matriz[posLatitud][posLongitud].cantidad = cantidad;
			  matriz[posLatitud][posLongitud].promedio = promedio;
		 }

	}
}

void InicializarMatriz(par matriz[TOTAL_LATITUD][TOTAL_LONGITUD])
{
    for (int i = 0; i < TOTAL_LATITUD; i++)
    {
        for (int j = 0; j < TOTAL_LONGITUD; j++)
        {
            matriz[i][j].cantidad = 0;
            matriz[i][j].promedio = 0.f;
        }
    }
}

void MostrarMatriz(par matriz[TOTAL_LATITUD][TOTAL_LONGITUD])
{
    for (int i = 0; i < TOTAL_LATITUD; i++)
    {
        for (int j = 0; j < TOTAL_LONGITUD; j++)
        {
            if (matriz[i][j].cantidad > 0) //Muestro solo valores de la matriz con datos cargados
            {
                cout << "(" << i << ", " << j << "): ";
                cout << "Cantidad: " << matriz[i][j].cantidad << ", ";
                cout << "Promedio: " << matriz[i][j].promedio << endl;
            }
        }
        cout << endl;
    }
}


//funciones del menu




void cargarRegistro()
{


}

void emitirReporte1()
{

}

void emitirReporte2()
{

}



void abrirMenu()
{
	par matriz[TOTAL_LATITUD][TOTAL_LONGITUD];

	//InicializarMatriz(matriz);


	char opcion;

	bool datos_validos;

	do
	{
		datos_validos = true;
		cout<<"------------------------"<<endl;
		cout<<"Ingrese opcion:"<<endl;
		cout<<"1.Cargar Registro"<<endl;
		cout<<"2.Cargar datos de prueba"<<endl;
		cout<<"3.Emitir reporte 1"<<endl;
		cout<<"4.Emitir reporte 2"<<endl;
		cout<<"5.Salir"<<endl;

		opcion = getche();
		getch();
		cout<<"\n------------------------"<<endl;



		if(opcion >= '1' && opcion <= '5' )
		{
			switch(opcion)
			{
			case '1':
				cargarRegistro();
				break;

			case '2':
				CargarDatosPrueba(matriz);
				MostrarMatriz(matriz);
				break;

			case '3':
				emitirReporte1();
				break;

			case '4':
				emitirReporte2();
				break;

			case '5':
				break;
			}

		}
		else
		{
			cout<<"Ingrese una opcion valida"<<endl;
			datos_validos = false;
		}


	}
	while((opcion>='1' && opcion<'5') || (!datos_validos) );


	//


}




int main()
{
	srand(time(NULL));


	abrirMenu();


	return 0;
}
