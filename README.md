# API Productos (Serverless + AWS Lambda + DynamoDB)

Este proyecto implementa una API REST para gestionar productos utilizando AWS Lambda, DynamoDB y Serverless Framework. Todas las funciones están protegidas con autenticación por token, verificada mediante el Lambda `ValidarTokenAcceso`.

## Tecnologías usadas
- **Python**
- **AWS Lambda**
- **AWS DynamoDB**
- **Serverless Framework**
- **boto3**

## Endpoints

| Método | Ruta                   | Descripción                     |
| :----- | :--------------------- | :------------------------------ |
| POST   | `/productos/crear`     | Crea un nuevo producto          |
| POST   | `/productos/listar`    | Lista productos (por tenant_id) |
| POST   | `/productos/buscar`    | Busca un producto específico    |
| PUT    | `/productos/modificar` | Modifica los datos del producto |
| DELETE | `/productos/eliminar`  | Elimina un producto             |

