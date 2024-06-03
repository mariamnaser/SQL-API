from typing import Any, Dict, List, Tuple, Union

import pymysql

# Type definitions
KV = Dict[str, Any]
Query = Tuple[str, List]

class DB:
	def __init__(self, host: str, port: int, user: str, password: str, database: str):
		conn = pymysql.connect(
			host=host,
			port=port,
			user=user,
			password=password,
			database=database,
			cursorclass=pymysql.cursors.DictCursor,
			autocommit=True,
		)
		self.conn = conn

	def get_cursor(self):
		return self.conn.cursor()
	def get_cursor(self):
		return self.conn.cursor()

	def execute_query(self, query: str, args: List, ret_result: bool) -> Union[List[KV], int]:
		cur = self.get_cursor()
		count = cur.execute(query, args=args)
		if ret_result:
			return cur.fetchall()
		else:
			return count

	@staticmethod
	def build_select_query(table: str, rows: List[str], filters: KV) -> Query:
		if rows:
			select_clause = ", ".join(rows)
		else:
			select_clause = "*"
		query = f"SELECT {select_clause} FROM {table}"
		parameters = []
		if filters:
			where_clauses = []
			for field, value in filters.items():
				where_clauses.append(f"{field} = %s")
				parameters.append(value)
			where_clause = " AND ".join(where_clauses)
			query += f" WHERE {where_clause}"
		return query, parameters

	def select(self, table: str, rows: List[str], filters: KV) -> List[KV]:
		query, parameter = self.build_select_query(table, rows, filters)
		result = self.execute_query(query, parameter, True)
		return result

	@staticmethod
	def build_insert_query(table: str, values: KV) -> Query:
		parameters = []
		if values:
			where_clauses = []
			string_holder = []
			for field, value in values.items():
				where_clauses.append(field)
				string_holder.append('%s')
				parameters.append(value)
			where_clause = ", ".join(where_clauses)
			string_hold = ", ".join(string_holder)
		query = f"INSERT INTO {table} ({where_clause}) VALUES ({string_hold})"
		return query, parameters

	def insert(self, table: str, values: KV) -> int:
		query, parameters = self.build_insert_query(table, values)
		result = self.execute_query(query, parameters, False)
		return result

	@staticmethod
	def build_update_query(table: str, values: KV, filters: KV) -> Query:
		parameters = []
		query = f"UPDATE {table}"
		if values:
			set_clauses = []
			for field, value in values.items():
				set_clauses.append(f"{field} = %s")
				parameters.append(value)
			set_clause = ", ".join(set_clauses)
			query += f" SET {set_clause}"
		if filters:
			where_clauses = []
			for field, value in filters.items():
				where_clauses.append(f"{field} = %s")
				parameters.append(value)
			where_clause = " AND ".join(where_clauses)
			query += f" WHERE {where_clause}"
		return query, parameters

	def update(self, table: str, values: KV, filters: KV) -> int:
		query, parameters = self.build_update_query(table, values, filters)
		result = self.execute_query(query, parameters, False)
		return result

	@staticmethod
	def build_delete_query(table: str, filters: KV) -> Query:
		parameters = []
		query = f"DELETE FROM {table}"
		if filters:
			where_clauses = []
			for field, value in filters.items():
				where_clauses.append(f"{field} = %s")
				parameters.append(value)
			where_clause = " AND ".join(where_clauses)
			query += f" WHERE {where_clause}"
		return query, parameters

	def delete(self, table: str, filters: KV) -> int:
		query, parameters = self.build_delete_query(table, filters)
		result = self.execute_query(query, parameters, False)
		return result
