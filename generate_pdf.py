import looker_sdk, configparser, time, os, PyPDF2

CONFIG = configparser.ConfigParser()
with open('looker.ini', 'r') as f:
    CONFIG.read_file(f)

sdk = looker_sdk.init40(config_file='looker.ini', section='Looker')

def getCategories():
  categories = []
  body = {
  "model": CONFIG['LookML']['model'],
  "view": CONFIG['LookML']['view'],
  "fields": [CONFIG['LookML']['field']],
  }
  response = eval(sdk.run_inline_query(result_format="json",body=body))
  for r in response:
    categories.append(r[CONFIG['LookML']['field']])
  return categories

def createRenderTask(filters):
  renders = []
  db_filter = CONFIG['LookML']['dashboard_filters'][:-1]
  for f in filters:
    body = {
              "dashboard_filters": f'''"{db_filter}{f}"''',
              "dashboard_style": "single_column"
            }
    response = sdk.create_dashboard_render_task(
    dashboard_id=CONFIG['LookML']['dashboard_id'],
    result_format=str(CONFIG['OutputSettings']['result_format']),
    body = body,
    width=CONFIG['OutputSettings']['width'],
    height=CONFIG['OutputSettings']['height'],
    pdf_paper_size="a4",
    long_tables=True)
    renders.append(response['id'])
  return renders

def waitUntilComplete(id):
  finished_renders = []
  total = 0
  for i in id:
    elapsed = 0.0
    delay = 1  # careful here to not overload the balancer
    while True:
        poll = sdk.render_task(i)
        if poll.status == "failure":
            print(poll)
            raise Exception(
                f'Render failed for Look'
            )
        elif poll.status == "success":
            break

        time.sleep(delay)
        elapsed += delay
    # print(f"Render task {i} completed in {elapsed} seconds")
    finished_renders.append(i)
    total += elapsed
  print(f"All render tasks completed in {total} seconds")
  return finished_renders


def produceFile(id):
  files = []
  for i in id:
    filename = f"{i}.pdf"
    result = sdk.render_task_results(i)
    with open(filename, "ab") as f:
      f.write(result)
      f.close()
      files.append(filename)
  return files


def mergePdf(files,filename):
  filename = filename
  mergeFile = PyPDF2.PdfFileMerger()
  for pdf in files:
    mergeFile.append(PyPDF2.PdfFileReader(pdf,'rb'))
    os.remove(pdf)
  mergeFile.write(filename)

def main():
  filename = "output.pdf"
  categories = getCategories()
  jobs = createRenderTask(categories)
  prod_id = waitUntilComplete(jobs)
  files = produceFile(prod_id)
  mergePdf(files,filename)

if __name__ == '__main__':
    main()
