"""
Georgia Dashboard Backend - Railway Deployment
Connects to SQL Server via Tailscale
"""
import os
import pymssql
import pandas as pd
from datetime import datetime
from decimal import Decimal
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from Vercel

def decimal_default(obj):
    """JSON encoder for Decimal and datetime objects"""
    if isinstance(obj, Decimal):
        return float(obj)
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def get_db_connection():
    """Create database connection via Tailscale"""
    return pymssql.connect(
        server=os.environ.get('DB_SERVER', '10.1.10.105'),
        user=os.environ.get('DB_USERNAME', 'amchranya'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_DATABASE', 'GAWDB'),
        port=int(os.environ.get('DB_PORT', '1433')),
        timeout=30,
        login_timeout=10,
        tds_version='7.0'
    )

def execute_query(query, params=None):
    """Execute query and return DataFrame"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()

        return pd.DataFrame(results, columns=columns)
    except Exception as e:
        print(f"Query error: {e}")
        return pd.DataFrame()

@app.route('/')
def home():
    """API info"""
    return jsonify({
        'name': 'Georgia Dashboard Backend',
        'status': 'running',
        'version': '1.0',
        'endpoints': {
            '/health': 'Database health check',
            '/api/test': 'Simple test endpoint',
            '/api/executive-summary': 'Executive dashboard metrics'
        }
    })

@app.route('/health')
def health():
    """Health check with database connectivity"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION as version, DB_NAME() as database")
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': {
                'connected': True,
                'database': result[1] if result else 'Unknown',
                'version': str(result[0])[:50] if result else 'Unknown'
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/test')
def api_test():
    """Simple test endpoint - no database required"""
    return jsonify({
        'success': True,
        'message': 'API is working!',
        'timestamp': datetime.now().isoformat(),
        'server_info': {
            'environment': os.environ.get('RAILWAY_ENVIRONMENT', 'unknown'),
            'region': os.environ.get('RAILWAY_REGION', 'unknown')
        }
    })

@app.route('/api/executive-summary')
def executive_summary():
    """Get executive summary metrics"""
    try:
        # Today's sales
        today_query = """
        SELECT ISNULL(SUM(extPrice), 0) as today_sales
        FROM puViewDailySales
        WHERE CONVERT(date, tranDate) = CONVERT(date, GETDATE())
        """
        today_result = execute_query(today_query)
        today_sales = float(today_result.iloc[0]['today_sales']) if not today_result.empty else 0

        # YTD Revenue
        ytd_query = """
        SELECT ISNULL(SUM(extPrice), 0) as ytd_revenue
        FROM puViewDailySales
        WHERE YEAR(tranDate) = YEAR(GETDATE())
        """
        ytd_result = execute_query(ytd_query)
        ytd_revenue = float(ytd_result.iloc[0]['ytd_revenue']) if not ytd_result.empty else 0

        # Customer count
        customer_query = """
        SELECT COUNT(DISTINCT custno) as customer_count
        FROM puViewDailySales
        WHERE tranDate >= DATEADD(day, -30, GETDATE())
        """
        customer_result = execute_query(customer_query)
        customer_count = int(customer_result.iloc[0]['customer_count']) if not customer_result.empty else 0

        # AR Balance
        ar_query = """
        SELECT ISNULL(SUM(balance), 0) as ar_balance
        FROM arcust
        WHERE balance > 0
        """
        ar_result = execute_query(ar_query)
        ar_balance = float(ar_result.iloc[0]['ar_balance']) if not ar_result.empty else 0

        return jsonify({
            'success': True,
            'data': {
                'today_sales': today_sales,
                'ytd_revenue': ytd_revenue,
                'customer_count': customer_count,
                'ar_balance': ar_balance,
                'timestamp': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
