mkdir -p ~/.streamlit/

printf "[server]\nport=%s\n enableCORS=false\n headless=true\n" "$PORT" > ~/.streamlit/config.toml