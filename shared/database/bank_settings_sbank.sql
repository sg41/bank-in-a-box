-- Override bank settings for sbank
INSERT INTO bank_settings (key, value) VALUES
  ('bank_code', 'sbank'),
  ('bank_name', 'Smart Bank'),
  ('public_address', 'http://localhost:8003'),
  ('capital', '3500000.00')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;

INSERT INTO bank_capital (bank_code, capital, initial_capital, total_deposits, total_loans)
VALUES ('sbank', 3500000.00, 3500000.00, 0, 0)
ON CONFLICT (bank_code) DO UPDATE SET capital = EXCLUDED.capital, initial_capital = EXCLUDED.initial_capital;