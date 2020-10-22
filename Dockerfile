FROM python:3.8
COPY auction auction
CMD ["python", "-m", "auction.main"]
