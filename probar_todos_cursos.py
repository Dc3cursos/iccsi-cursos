#!/usr/bin/env python
"""
Script para probar el endpoint que muestra todos los cursos
"""
import requests
import json

def probar_todos_cursos():
    """Probar endpoint que muestra todos los cursos"""
    base_url = "http://127.0.0.1:8000/api"
    
    print("🧪 PROBANDO ENDPOINT DE TODOS LOS CURSOS")
    print("=" * 50)
    
    # 1. Login para obtener token
    print("\n1️⃣ Iniciando sesión...")
    try:
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        response = requests.post(f"{base_url}/auth/login/", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            token = data['access']
            print("   ✅ Login exitoso!")
            
            # 2. Probar endpoint de todos los cursos
            print("\n2️⃣ Probando endpoint de todos los cursos...")
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(f"{base_url}/cursos/todos/", headers=headers)
            
            if response.status_code == 200:
                cursos_data = response.json()
                cursos = cursos_data.get('cursos', [])
                total = cursos_data.get('total', 0)
                mensaje = cursos_data.get('mensaje', '')
                
                print(f"   ✅ Respuesta exitosa!")
                print(f"   📚 Total de cursos: {total}")
                print(f"   📋 Cursos en respuesta: {len(cursos)}")
                print(f"   💬 Mensaje: {mensaje}")
                
                if cursos:
                    print(f"\n3️⃣ Primeros 3 cursos:")
                    for i, curso in enumerate(cursos[:3]):
                        print(f"   {i+1}. ID: {curso['id']} - {curso['nombre']}")
                        print(f"      Duración: {curso['duracion_horas']} horas")
                        org = curso.get('organizacion', {})
                        org_nombre = org.get('nombre', 'Sin organización') if org else 'Sin organización'
                        print(f"      Organización: {org_nombre}")
                        print()
                
                # 3. Comparar con endpoint normal
                print("\n4️⃣ Comparando con endpoint normal...")
                response_normal = requests.get(f"{base_url}/cursos/", headers=headers)
                
                if response_normal.status_code == 200:
                    normal_data = response_normal.json()
                    normal_count = len(normal_data.get('results', []))
                    print(f"   📊 Endpoint normal: {normal_count} cursos")
                    print(f"   📊 Endpoint todos: {len(cursos)} cursos")
                    print(f"   📊 Total real: {total} cursos")
                    
                    if len(cursos) == total:
                        print("   ✅ ¡Perfecto! Se obtuvieron todos los cursos")
                    else:
                        print(f"   ⚠️ Diferencia: {total - len(cursos)} cursos no mostrados")
                else:
                    print(f"   ❌ Error en endpoint normal: {response_normal.status_code}")
                    
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                
        else:
            print(f"   ❌ Error en login: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 RESUMEN:")
    print("   - Endpoint /todos/ debe mostrar todos los cursos")
    print("   - Endpoint normal muestra solo 100 por página")
    print("   - App de escritorio ahora usa /todos/")

if __name__ == "__main__":
    probar_todos_cursos()
