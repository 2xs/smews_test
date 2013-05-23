/*
<generator>
	<handlers doPostOut="doPostOut" doPostIn="doPostIn"/>
	<content-types>
		<content-type type="application/octet-stream" />
	</content-types>
	
</generator>
*/

struct file_t {
	char *   filename;
	uint16_t size;
};

static char doPostIn(uint8_t content_type, uint8_t call_number, char *filename, void **post_data) {
	uint16_t i  = 0;
	short    value;

	if(!filename)  return 1;

	if(*post_data) return 1;

	/* counting filename size */
	while(filename[i++] != '\0');

	struct file_t *file = mem_alloc(sizeof(struct file_t));
	if(!file)
		return 1;
	file->filename = mem_alloc(sizeof(char) * i);

	/* Copying filename */
	i = 0;
	do {
		file->filename[i] = filename[i];
	}while(filename[i++] != '\0');

	/* counting bytes in file */
	i = 0;
	while((value = in()) != -1)
		i++;
	file->size = i;

	*post_data = file;

	return 1;
}

static char doPostOut(uint8_t content_type, void *data) {
	uint16_t i;

	if(data) {
		out_str("The file \"");
		out_str( ((struct file_t *)data)->filename);
		out_str("\" contains ");
		out_uint( ((struct file_t *)data)->size);
		out_str(" characters.");

		// Clean up memory
		//
		i = 0;
		// releasing filename
		while( ((struct file_t *)data)->filename[i++] != '\0');

		mem_free(((struct file_t *)data)->filename, sizeof(char) * i);

		// releasing file
		mem_free(data, sizeof(struct file_t));
	} else
		out_str("No data file");

}
