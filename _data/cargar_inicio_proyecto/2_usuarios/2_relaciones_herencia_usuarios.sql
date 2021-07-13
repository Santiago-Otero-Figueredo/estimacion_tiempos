INSERT INTO public.usuarios_empresa (usuario_ptr_id) VALUES (1);
INSERT INTO public.usuarios_empresa (usuario_ptr_id) VALUES (11);

SELECT pg_catalog.setval('public.usuarios_usuario_id_seq', 12, false);

INSERT INTO public.usuarios_empleado (usuario_ptr_id) VALUES (2);
INSERT INTO public.usuarios_empleado (usuario_ptr_id) VALUES (3);
INSERT INTO public.usuarios_empleado (usuario_ptr_id) VALUES (4);
INSERT INTO public.usuarios_empleado (usuario_ptr_id) VALUES (5);
INSERT INTO public.usuarios_empleado (usuario_ptr_id) VALUES (6);
INSERT INTO public.usuarios_empleado (usuario_ptr_id) VALUES (7);
INSERT INTO public.usuarios_empleado (usuario_ptr_id) VALUES (8);
INSERT INTO public.usuarios_empleado (usuario_ptr_id) VALUES (9);
INSERT INTO public.usuarios_empleado (usuario_ptr_id) VALUES (10);

INSERT INTO public.usuarios_administrador (empleado_ptr_id) VALUES (2);

INSERT INTO public.usuarios_trabajador (empleado_ptr_id) VALUES (3);
INSERT INTO public.usuarios_trabajador (empleado_ptr_id) VALUES (4);
INSERT INTO public.usuarios_trabajador (empleado_ptr_id) VALUES (5);
INSERT INTO public.usuarios_trabajador (empleado_ptr_id) VALUES (6);
INSERT INTO public.usuarios_trabajador (empleado_ptr_id) VALUES (7);
INSERT INTO public.usuarios_trabajador (empleado_ptr_id) VALUES (8);
INSERT INTO public.usuarios_trabajador (empleado_ptr_id) VALUES (9);
INSERT INTO public.usuarios_trabajador (empleado_ptr_id) VALUES (10);



