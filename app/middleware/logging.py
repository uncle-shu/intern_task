import logging
import time

from fastapi import Request, Response

async def log_requests(request: Request, call_next):
  raw_path = '{}{}{}'.format(request.url.path,
                             '?' if request.url.query else '',
                             request.url.query)
  request.state.start_time = time.time()

  response: Response = await call_next(request)

  process_time = (time.time() - request.state.start_time) * 1000
  formatted_process_time = '{0:.2f}'.format(process_time)
  logging.info('UserID: %s - %s %s -%sms',
               request.headers.get("user-id"),
               request.method,
               raw_path,
               formatted_process_time)

  return response