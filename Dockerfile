#build application
FROM python:3.11-alpine AS build
RUN pip install --root-user-action=ignore --upgrade pip
COPY . /ems
WORKDIR /ems
RUN pip install --root-user-action=ignore build
RUN python3 -m build --wheel
RUN ls -lrt /ems/dist

#run application
FROM python:3.11-alpine AS run
RUN pip install --root-user-action=ignore --upgrade pip
COPY --from=build /ems/dist/*.whl .
COPY requirements.txt .
RUN pip install --root-user-action=ignore --no-cache-dir -r requirements.txt
RUN pip install --root-user-action=ignore *.whl
RUN mkdir /resources
COPY ./ems/resources/application.yaml /resources/application.yaml
RUN ln -sv /usr/bin/python3.11 /usr/bin/python3
ENTRYPOINT [ "ems"]
