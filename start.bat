@echo off

rem Load environment variables
for /f "tokens=1,2 delims==" %%G in (.env) do set %%G=%%H

rem Build Docker image
docker build -t localgpt .

rem Run Docker container
docker run -dp 8000:8000 ^
  -e OPENAI_API_KEY="%OPENAI_API_KEY%" ^
  -e ANTHROPIC_API_KEY="%ANTHROPIC_API_KEY%" ^
  -e EXA_API_KEY="%EXA_API_KEY%" ^
  -e MODEL_TYPE="%MODEL_TYPE%" ^
  localgpt