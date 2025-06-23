# 1. Use an official Python base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR C:\Users\anush\Desktop\Anushree_Agrawal_Projects\BookHub_Internship

# 3. Copy all project files into the container
COPY . .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose the port Uvicorn will run on
EXPOSE 8000

# 6. Start the FastAPI server when the container runs
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
 
