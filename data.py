import pandas as pd
from sqlalchemy import create_engine
import logging

def get_top_drugs():
    query_template = """
    SELECT 
        p.product_name,
        SUM(u.number_of_prescriptions) as number_of_prescriptions,
        SUM(u.total_amount_reimbursed) as total_amount_reimbursed,
        SUM(u.medicaid_amount_reimbursed) as medicaid_amount_reimbursed
    FROM utilization u
    INNER JOIN product p ON u.product_id = p.product_id
    INNER JOIN state s ON u.state_id = s.state_id
    WHERE s.state = %(state)s                  
    GROUP BY p.product_name
    ORDER BY total_amount_reimbursed DESC
    LIMIT 10
    """
    
    try: 
        engine = create_engine('mysql+mysqlconnector://root:password@localhost/drugutilization')
        
        # Fetch data for Illinois
        il_data = pd.read_sql_query(query_template, engine, params = {'state': 'IL'})
        
        # Fetch data for Alaska
        ak_data = pd.read_sql_query(query_template, engine, params={'state': 'AK'})

        il_data_dict = il_data.to_dict('records')
        ak_data_dict = ak_data.to_dict('records')
        
        # Create dictionary with separate keys for Illinois and Alaska data
        data_dict = {'IL': il_data_dict, 'AK': ak_data_dict}
        
        return data_dict
    except Exception as e:
        logging.error(f"Error fetching top drugs: {e}")
        return None
    finally:
        # Close the database connection
        engine.dispose()
